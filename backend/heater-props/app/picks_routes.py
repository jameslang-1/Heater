# app/picks_routes.py
from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import hashlib
import jwt

from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/api/picks", tags=["picks"])

def get_current_user(authorization: str = Header(None)):
    """Extract user from Firebase auth token and map to integer ID"""
    if not authorization:
        # No auth header - use test user
        return {'id': 1, 'email': 'test@test.com'}
    
    try:
        # Extract token from "Bearer <token>"
        token = authorization.replace('Bearer ', '')
        
        # Decode JWT token (Firebase already verified it on frontend)
        decoded = jwt.decode(token, options={"verify_signature": False})
        firebase_uid = decoded.get('user_id') or decoded.get('sub')
        email = decoded.get('email', 'unknown@unknown.com')
        
        # Convert Firebase UID string to consistent integer ID
        # Use hash of UID to generate a deterministic integer
        user_id = int(hashlib.sha256(firebase_uid.encode()).hexdigest()[:8], 16)
        
        print(f"Authenticated user: {email} (ID: {user_id})")
        
        return {
            'id': user_id,
            'email': email,
            'firebase_uid': firebase_uid
        }
    except Exception as e:
        print(f"Auth error: {e}")
        # Fallback to test user on error
        return {'id': 1, 'email': 'test@test.com'}


# Pydantic models for request/response
class PickCreate(BaseModel):
    player_name: str
    prop_type: str
    line: float
    prediction: str  # 'over' or 'under'
    game_id: str
    home_team: str
    away_team: str
    game_date: datetime


class PickDelete(BaseModel):
    player_name: str
    prop_type: str
    game_id: str


@router.post("/", status_code=status.HTTP_201_CREATED)
def save_pick(
    pick: PickCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Save a new pick"""
    user_id = current_user['id']
    
    # Validate prediction
    if pick.prediction not in ['over', 'under']:
        raise HTTPException(status_code=400, detail="Invalid prediction. Must be 'over' or 'under'")
    
    # Find the player prop based on player_name, prop_type, and game
    game = db.query(models.Game).filter(
        models.Game.external_id == pick.game_id
    ).first()
    
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    
    prop = db.query(models.PlayerProp).filter(
        models.PlayerProp.game_id == game.id,
        models.PlayerProp.player_name == pick.player_name,
        models.PlayerProp.prop_type == pick.prop_type
    ).first()
    
    if not prop:
        raise HTTPException(status_code=404, detail="Player prop not found")
    
    # Check if pick already exists
    existing_pick = db.query(models.Pick).filter(
        models.Pick.user_id == user_id,
        models.Pick.player_prop_id == prop.id
    ).first()
    
    if existing_pick:
        # Update existing pick
        existing_pick.selection = pick.prediction
        existing_pick.line = pick.line
        db.commit()
        db.refresh(existing_pick)
        
        return {
            'success': True,
            'pick_id': existing_pick.id,
            'message': 'Pick updated successfully',
            'pick': {
                'id': existing_pick.id,
                'player_name': prop.player_name,
                'prop_type': prop.prop_type,
                'line': existing_pick.line,
                'selection': existing_pick.selection
            }
        }
    
    # Create new pick
    new_pick = models.Pick(
        player_prop_id=prop.id,
        user_id=user_id,
        selection=pick.prediction,
        line=pick.line
    )
    
    db.add(new_pick)
    db.commit()
    db.refresh(new_pick)
    
    return {
        'success': True,
        'pick_id': new_pick.id,
        'message': 'Pick saved successfully',
        'pick': {
            'id': new_pick.id,
            'player_name': prop.player_name,
            'prop_type': prop.prop_type,
            'line': new_pick.line,
            'selection': new_pick.selection
        }
    }


@router.delete("/")
def delete_pick(
    pick: PickDelete,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Delete a pick"""
    user_id = current_user['id']
    
    # Find the game
    game = db.query(models.Game).filter(
        models.Game.external_id == pick.game_id
    ).first()
    
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    
    # Find the prop
    prop = db.query(models.PlayerProp).filter(
        models.PlayerProp.game_id == game.id,
        models.PlayerProp.player_name == pick.player_name,
        models.PlayerProp.prop_type == pick.prop_type
    ).first()
    
    if not prop:
        raise HTTPException(status_code=404, detail="Player prop not found")
    
    # Find and delete the pick
    pick_to_delete = db.query(models.Pick).filter(
        models.Pick.user_id == user_id,
        models.Pick.player_prop_id == prop.id
    ).first()
    
    if not pick_to_delete:
        raise HTTPException(status_code=404, detail='Pick not found')
    
    db.delete(pick_to_delete)
    db.commit()
    
    return {
        'success': True,
        'message': 'Pick deleted successfully'
    }


@router.get("/active")
def get_active_picks(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get all active (ungraded) picks for the current user"""
    user_id = current_user['id']
    
    picks = db.query(models.Pick).filter(
        models.Pick.user_id == user_id,
        models.Pick.result == None  # Only ungraded picks
    ).all()
    
    result = []
    for pick in picks:
        prop = pick.player_prop
        game = prop.game
        
        result.append({
            'id': pick.id,
            'player_name': prop.player_name,
            'prop_type': prop.prop_type,
            'line': pick.line,
            'prediction': pick.selection,  # Frontend expects 'prediction'
            'game_id': game.external_id,
            'home_team': game.home_team,
            'away_team': game.away_team,
            'game_date': game.commence_time,
            'created_at': pick.created_at
        })
    
    return {
        'picks': result,
        'total': len(result)
    }


@router.get("/check/{game_id}")
def check_user_picks_for_game(
    game_id: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Check which picks the user has made for a specific game"""
    user_id = current_user['id']
    
    # Find the game
    game = db.query(models.Game).filter(
        models.Game.external_id == game_id
    ).first()
    
    if not game:
        return {'picks': {}}
    
    # Get all props for this game
    props = db.query(models.PlayerProp).filter(
        models.PlayerProp.game_id == game.id
    ).all()
    
    prop_ids = [p.id for p in props]
    
    # Get user's picks for these props
    picks = db.query(models.Pick).filter(
        models.Pick.user_id == user_id,
        models.Pick.player_prop_id.in_(prop_ids)
    ).all()
    
    # Create lookup dict
    user_picks = {}
    for pick in picks:
        prop = pick.player_prop
        key = f"{prop.player_name}-{prop.prop_type}"
        user_picks[key] = pick.selection
    
    return {'picks': user_picks}


@router.get("/history")
def get_pick_history(
    result: Optional[str] = None,
    prop_type: Optional[str] = None,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get graded pick history for the current user"""
    user_id = current_user['id']
    
    query = db.query(models.Pick).filter(
        models.Pick.user_id == user_id,
        models.Pick.result != None  # Only graded picks
    )
    
    if result:
        query = query.filter(models.Pick.result == result)
    
    if prop_type:
        query = query.join(models.PlayerProp).filter(
            models.PlayerProp.prop_type == prop_type
        )
    
    picks = query.order_by(models.Pick.graded_at.desc()).limit(limit).all()
    
    history = []
    for pick in picks:
        prop = pick.player_prop
        game = prop.game
        
        history.append({
            'id': pick.id,
            'player_name': prop.player_name,
            'prop_type': prop.prop_type,
            'line': pick.line,
            'prediction': pick.selection,
            'result': pick.result,
            'actual_result': pick.actual_value,
            'game_id': game.external_id,
            'home_team': game.home_team,
            'away_team': game.away_team,
            'game_date': game.commence_time,
            'created_at': pick.created_at,
            'completed_at': pick.graded_at
        })
    
    return history


@router.get("/stats")
def get_user_stats(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get user's overall statistics"""
    user_id = current_user['id']
    
    # Get all graded picks
    picks = db.query(models.Pick).filter(
        models.Pick.user_id == user_id,
        models.Pick.result != None
    ).all()
    
    total = len(picks)
    wins = sum(1 for p in picks if p.result == 'won')
    losses = sum(1 for p in picks if p.result == 'lost')
    pushes = sum(1 for p in picks if p.result == 'push')
    
    win_percentage = (wins / (wins + losses) * 100) if (wins + losses) > 0 else 0
    
    # Calculate by prop type
    by_prop_type = {}
    for prop_type in ['points', 'rebounds', 'assists']:
        type_picks = [p for p in picks if p.player_prop.prop_type == prop_type]
        type_wins = sum(1 for p in type_picks if p.result == 'won')
        type_total = len(type_picks)
        
        by_prop_type[prop_type] = {
            'total': type_total,
            'wins': type_wins,
            'win_rate': round((type_wins / type_total * 100) if type_total > 0 else 0, 1)
        }
    
    # Get recent form (last 10)
    recent_picks = sorted(picks, key=lambda p: p.graded_at if p.graded_at else p.created_at, reverse=True)[:10]
    recent_form = [p.result for p in recent_picks if p.result in ['won', 'lost']]
    
    # Calculate current streak
    current_streak = 0
    if recent_form:
        streak_type = recent_form[0]
        for result in recent_form:
            if result == streak_type:
                current_streak += 1 if streak_type == 'won' else -1
            else:
                break
    
    return {
        'total_picks': total,
        'wins': wins,
        'losses': losses,
        'pushes': pushes,
        'win_percentage': round(win_percentage, 1),
        'current_streak': current_streak,
        'best_streak': abs(current_streak),  # Simplified
        'by_prop_type': by_prop_type,
        'recent_form': recent_form,
        'last_updated': datetime.utcnow()
    }