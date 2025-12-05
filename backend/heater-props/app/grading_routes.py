# app/grading_routes.py
# Add these routes to your FastAPI app

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from app.database import get_db
from app.grading_service import grading_service
from app import models

router = APIRouter(prefix="/api/grading", tags=["grading"])

@router.post("/grade-game/{game_id}")
def grade_game_picks(game_id: int, db: Session = Depends(get_db)):
    """
    Grade all picks for a specific completed game
    """
    # Get the game
    game = db.query(models.Game).filter(models.Game.id == game_id).first()
    
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    
    # Grade picks for this game
    result = grading_service.grade_picks_for_game(db, game)
    
    return result

@router.post("/grade-all")
def grade_all_picks(db: Session = Depends(get_db)):
    """
    Grade picks for all completed games
    
    This will check all games that have passed and grade any ungraded picks
    """
    results = grading_service.grade_all_completed_games(db)
    
    return {
        "message": "Grading completed",
        "games_processed": len(results),
        "results": results
    }

@router.get("/pick-results")
def get_pick_results(
    user_id: int = None,
    result: str = None,  # 'won', 'lost', 'push'
    db: Session = Depends(get_db)
):
    """
    Get all graded picks with optional filters
    """
    query = db.query(models.Pick).filter(models.Pick.result != None)
    
    if user_id:
        query = query.filter(models.Pick.user_id == user_id)
    
    if result:
        query = query.filter(models.Pick.result == result)
    
    picks = query.all()
    
    return {
        "total": len(picks),
        "picks": picks
    }

@router.get("/user-record/{user_id}")
def get_user_record(user_id: int, db: Session = Depends(get_db)):
    """
    Get win/loss record for a specific user
    """
    picks = db.query(models.Pick).filter(
        models.Pick.user_id == user_id,
        models.Pick.result != None
    ).all()
    
    won = sum(1 for p in picks if p.result == 'won')
    lost = sum(1 for p in picks if p.result == 'lost')
    push = sum(1 for p in picks if p.result == 'push')
    
    total = won + lost + push
    win_pct = (won / (won + lost) * 100) if (won + lost) > 0 else 0
    
    return {
        "user_id": user_id,
        "record": {
            "won": won,
            "lost": lost,
            "push": push,
            "total": total
        },
        "win_percentage": round(win_pct, 1),
        "pending": db.query(models.Pick).filter(
            models.Pick.user_id == user_id,
            models.Pick.result == None
        ).count()
    }

@router.get("/leaderboard")
def get_leaderboard(
    timeframe: str = "overall",
    current_user_id: int = None,
    db: Session = Depends(get_db)
):
    """
    Get leaderboard of all users ranked by win percentage
    """
    from datetime import datetime, timedelta
    
    # Calculate date filter based on timeframe
    date_filter = None
    if timeframe == "week":
        date_filter = datetime.utcnow() - timedelta(days=7)
    elif timeframe == "month":
        date_filter = datetime.utcnow() - timedelta(days=30)
    
    # Get all users with graded picks
    query = db.query(models.Pick.user_id).filter(
        models.Pick.result != None
    )
    
    if date_filter:
        query = query.filter(models.Pick.graded_at >= date_filter)
    
    users = query.distinct().all()
    
    leaderboard = []
    current_user_found = False
    
    for (user_id,) in users:
        if user_id is None:
            continue
        
        # Skip test data for current user (user_id 1-5 are test users)
        if user_id == current_user_id and user_id <= 5:
            current_user_found = True
            continue
            
        # Get picks for this user
        picks_query = db.query(models.Pick).filter(
            models.Pick.user_id == user_id,
            models.Pick.result != None
        )
        
        if date_filter:
            picks_query = picks_query.filter(models.Pick.graded_at >= date_filter)
        
        picks = picks_query.all()
        
        won = sum(1 for p in picks if p.result == 'won')
        lost = sum(1 for p in picks if p.result == 'lost')
        push = sum(1 for p in picks if p.result == 'push')
        
        if (won + lost) > 0:
            win_rate = round((won / (won + lost)) * 100, 1)
            
            # Calculate streak
            streak = calculate_streak(picks)
            
            leaderboard.append({
                "user_id": str(user_id),
                "wins": won,
                "losses": lost,
                "push": push,
                "total": won + lost + push,
                "win_rate": win_rate,
                "streak": streak,
                "is_user": user_id == current_user_id
            })
            
            if user_id == current_user_id:
                current_user_found = True
    
    # Sort by wins first, then win rate
    leaderboard.sort(key=lambda x: (x['wins'], x['win_rate']), reverse=True)
    
    # Add ranks
    for idx, entry in enumerate(leaderboard, 1):
        entry['rank'] = idx
    
    # If current user not found (no picks yet), add them with 0-0 record
    if current_user_id and not current_user_found:
        leaderboard.append({
            "user_id": str(current_user_id),
            "wins": 0,
            "losses": 0,
            "push": 0,
            "total": 0,
            "win_rate": 0.0,
            "streak": "0",
            "is_user": True,
            "rank": len(leaderboard) + 1
        })
    
    # Find current user rank
    current_user_rank = None
    if current_user_id:
        for entry in leaderboard:
            if entry['user_id'] == str(current_user_id):
                current_user_rank = entry['rank']
                break
    
    return {
        "leaderboard": leaderboard,
        "current_user_rank": current_user_rank,
        "total_users": len(leaderboard)
    }

def calculate_streak(picks: list) -> str:
    """Calculate current win/loss streak"""
    if not picks:
        return "0"
    
    # Sort by graded_at descending (most recent first)
    sorted_picks = sorted(picks, key=lambda p: p.graded_at, reverse=True)
    
    # Ignore pushes for streak calculation
    relevant_picks = [p for p in sorted_picks if p.result in ['won', 'lost']]
    
    if not relevant_picks:
        return "0"
    
    current_result = relevant_picks[0].result
    streak_count = 1
    
    for pick in relevant_picks[1:]:
        if pick.result == current_result:
            streak_count += 1
        else:
            break
    
    streak_letter = "W" if current_result == "won" else "L"
    return f"{streak_letter}{streak_count}"