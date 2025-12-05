# app/picks_routes.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

from app.database import get_db

router = APIRouter(prefix="/api/picks", tags=["picks"])

# Temporary auth placeholder - we'll add Firebase auth after testing
def get_current_user():
    """Temporary: returns a test user for testing"""
    # TODO: Replace with Firebase auth verification
    return {'id': 'test_user_123', 'email': 'test@test.com', 'firebase_uid': 'test_uid'}


# Pydantic models for request/response
class PickCreate(BaseModel):
    player_name: str
    prop_type: str  # 'points', 'rebounds', 'assists'
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


class PickCheck(BaseModel):
    game_id: str


class PickResponse(BaseModel):
    id: int
    player_name: str
    prop_type: str
    line: float
    prediction: str
    game_id: str
    home_team: str
    away_team: str
    game_date: datetime
    created_at: datetime


class PickHistoryResponse(BaseModel):
    id: int
    player_name: str
    prop_type: str
    line: float
    prediction: str
    game_id: str
    home_team: str
    away_team: str
    game_date: datetime
    actual_result: Optional[float]
    result: Optional[str]
    created_at: datetime
    completed_at: datetime


class UserStatsResponse(BaseModel):
    total_picks: int
    wins: int
    losses: int
    pushes: int
    win_percentage: float
    current_streak: int
    best_streak: int
    by_prop_type: dict
    recent_form: List[str]
    last_updated: datetime


@router.post("/", status_code=status.HTTP_201_CREATED)
def save_pick(
    pick: PickCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Save a new pick or update existing pick"""
    user_id = current_user['id']
    
    # Validate prediction
    if pick.prediction not in ['over', 'under']:
        raise HTTPException(status_code=400, detail="Invalid prediction value")
    
    # Validate prop_type
    if pick.prop_type not in ['points', 'rebounds', 'assists']:
        raise HTTPException(status_code=400, detail="Invalid prop type")
    
    # Get raw connection from SQLAlchemy session
    connection = db.connection().connection
    cursor = connection.cursor()
    
    try:
        # Check if pick already exists
        cursor.execute('''
            SELECT id FROM picks 
            WHERE user_id = ? AND player_name = ? AND prop_type = ? AND game_id = ?
        ''', (user_id, pick.player_name, pick.prop_type, pick.game_id))
        
        existing_pick = cursor.fetchone()
        
        if existing_pick:
            # Update existing pick
            cursor.execute('''
                UPDATE picks 
                SET line = ?, prediction = ?
                WHERE id = ?
            ''', (pick.line, pick.prediction, existing_pick[0]))
            pick_id = existing_pick[0]
        else:
            # Insert new pick
            cursor.execute('''
                INSERT INTO picks (
                    user_id, player_name, prop_type, line, prediction,
                    game_id, home_team, away_team, game_date
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                user_id, pick.player_name, pick.prop_type, pick.line,
                pick.prediction, pick.game_id, pick.home_team, 
                pick.away_team, pick.game_date
            ))
            pick_id = cursor.lastrowid
        
        connection.commit()
        
        return {
            'success': True,
            'pick_id': pick_id,
            'message': 'Pick saved successfully'
        }
        
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/")
def delete_pick(
    pick: PickDelete,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Delete a pick"""
    user_id = current_user['id']
    # Get raw connection from SQLAlchemy session
    connection = db.connection().connection
    cursor = connection.cursor()
    
    try:
        cursor.execute('''
            DELETE FROM picks 
            WHERE user_id = ? AND player_name = ? AND prop_type = ? AND game_id = ?
        ''', (user_id, pick.player_name, pick.prop_type, pick.game_id))
        
        connection.commit()
        
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail='Pick not found')
        
        return {
            'success': True,
            'message': 'Pick deleted successfully'
        }
        
    except HTTPException:
        raise
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/active", response_model=List[PickResponse])
def get_active_picks(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get all active picks for the current user"""
    user_id = current_user['id']
    # Get raw connection from SQLAlchemy session
    connection = db.connection().connection
    cursor = connection.cursor()
    
    cursor.execute('''
        SELECT 
            id, player_name, prop_type, line, prediction,
            game_id, home_team, away_team, game_date, created_at
        FROM picks
        WHERE user_id = ?
        ORDER BY game_date ASC
    ''', (user_id,))
    
    picks = []
    for row in cursor.fetchall():
        picks.append({
            'id': row[0],
            'player_name': row[1],
            'prop_type': row[2],
            'line': row[3],
            'prediction': row[4],
            'game_id': row[5],
            'home_team': row[6],
            'away_team': row[7],
            'game_date': row[8],
            'created_at': row[9]
        })
    
    return picks


@router.post("/check")
def check_user_picks(
    check: PickCheck,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Check which picks the user has made for specific props"""
    user_id = current_user['id']
    # Get raw connection from SQLAlchemy session
    connection = db.connection().connection
    cursor = connection.cursor()
    
    cursor.execute('''
        SELECT player_name, prop_type, prediction
        FROM picks
        WHERE user_id = ? AND game_id = ?
    ''', (user_id, check.game_id))
    
    user_picks = {}
    for row in cursor.fetchall():
        key = f"{row[0]}-{row[1]}"
        user_picks[key] = row[2]
    
    return {'picks': user_picks}


@router.get("/history", response_model=List[PickHistoryResponse])
def get_pick_history(
    result: Optional[str] = None,
    prop_type: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get pick history for the current user"""
    user_id = current_user['id']
    # Get raw connection from SQLAlchemy session
    connection = db.connection().connection
    cursor = connection.cursor()
    
    query = '''
        SELECT 
            id, player_name, prop_type, line, prediction,
            game_id, home_team, away_team, game_date,
            actual_result, result, created_at, completed_at
        FROM pick_history
        WHERE user_id = ?
    '''
    params = [user_id]
    
    if result:
        query += ' AND result = ?'
        params.append(result)
    
    if prop_type:
        query += ' AND prop_type = ?'
        params.append(prop_type)
    
    query += ' ORDER BY completed_at DESC LIMIT ? OFFSET ?'
    params.extend([limit, offset])
    
    cursor.execute(query, params)
    
    history = []
    for row in cursor.fetchall():
        history.append({
            'id': row[0],
            'player_name': row[1],
            'prop_type': row[2],
            'line': row[3],
            'prediction': row[4],
            'game_id': row[5],
            'home_team': row[6],
            'away_team': row[7],
            'game_date': row[8],
            'actual_result': row[9],
            'result': row[10],
            'created_at': row[11],
            'completed_at': row[12]
        })
    
    return history


@router.get("/stats", response_model=UserStatsResponse)
def get_user_stats(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get user's overall statistics"""
    user_id = current_user['id']
    # Get raw connection from SQLAlchemy session
    connection = db.connection().connection
    cursor = connection.cursor()
    
    # Get or create user stats
    cursor.execute('SELECT * FROM user_stats WHERE user_id = ?', (user_id,))
    stats = cursor.fetchone()
    
    if not stats:
        # Create initial stats record
        cursor.execute('INSERT INTO user_stats (user_id) VALUES (?)', (user_id,))
        connection.commit()
        
        cursor.execute('SELECT * FROM user_stats WHERE user_id = ?', (user_id,))
        stats = cursor.fetchone()
    
    # Calculate win percentage
    total_picks = stats[2]
    wins = stats[3]
    win_percentage = (wins / total_picks * 100) if total_picks > 0 else 0
    
    # Get recent form (last 10 picks)
    cursor.execute('''
        SELECT result FROM pick_history
        WHERE user_id = ?
        ORDER BY completed_at DESC
        LIMIT 10
    ''', (user_id,))
    
    recent_results = [row[0] for row in cursor.fetchall()]
    
    return {
        'total_picks': stats[2],
        'wins': stats[3],
        'losses': stats[4],
        'pushes': stats[5],
        'win_percentage': round(win_percentage, 1),
        'current_streak': stats[11],
        'best_streak': stats[12],
        'by_prop_type': {
            'points': {
                'total': stats[6],
                'wins': stats[7],
                'win_rate': round((stats[7] / stats[6] * 100) if stats[6] > 0 else 0, 1)
            },
            'rebounds': {
                'total': stats[8],
                'wins': stats[9],
                'win_rate': round((stats[9] / stats[8] * 100) if stats[8] > 0 else 0, 1)
            },
            'assists': {
                'total': stats[10],
                'wins': stats[11],
                'win_rate': round((stats[11] / stats[10] * 100) if stats[10] > 0 else 0, 1)
            }
        },
        'recent_form': recent_results,
        'last_updated': stats[13]
    }