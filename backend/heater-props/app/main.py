# app/main.py
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta

from app.database import get_db, engine, Base
from app import models, schemas, crud
from app.odds_service import stats_service
from app.picks_routes import router as picks_router

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Basketball Props API", version="1.0.0")

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include picks router
app.include_router(picks_router)

@app.get("/")
def root():
    return {"message": "Basketball Props API", "version": "1.0.0"}

@app.get("/api/games", response_model=schemas.GameListResponse)
def get_games(
    days_ahead: int = 14,
    db: Session = Depends(get_db)
):
    """Get upcoming NBA games with player props"""
    games = crud.get_upcoming_games(db, days_ahead=days_ahead)
    
    return {
        "games": games,
        "total": len(games)
    }

@app.get("/api/games/{game_id}", response_model=schemas.GameResponse)
def get_game(game_id: int, db: Session = Depends(get_db)):
    """Get a specific game with all its player props"""
    game = db.query(models.Game).filter(models.Game.id == game_id).first()
    
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    
    return game

@app.get("/api/player-props/{player_name}")
def get_player_props(
    player_name: str,
    prop_type: str = None,
    db: Session = Depends(get_db)
):
    """Get all props for a specific player"""
    props = crud.get_props_by_player(db, player_name, prop_type)
    
    if not props:
        raise HTTPException(status_code=404, detail="No props found for this player")
    
    return {"player_name": player_name, "props": props}

@app.get("/api/update-odds")
def update_odds(db: Session = Depends(get_db)):
    """
    Fetch latest games and generate projections
    """
    try:
        # Fetch upcoming games
        print("Fetching upcoming games...")
        games_data = stats_service.fetch_schedule(days_ahead=14)
        
        if not games_data:
            return {"message": "No games data received", "updated": 0}
        
        print(f"Found {len(games_data)} games")
        updated_count = 0
        
        for game_data in games_data:
            # Parse game info
            game_info = stats_service.parse_game_data(game_data)
            
            # Check if game already exists
            existing_game = crud.get_game_by_external_id(db, game_info['external_id'])
            
            if existing_game:
                # Update existing game
                existing_game.home_team = game_info['home_team']
                existing_game.away_team = game_info['away_team']
                existing_game.commence_time = game_info['commence_time']
                existing_game.updated_at = datetime.utcnow()
                
                # Delete old props
                crud.delete_game_props(db, existing_game.id)
                game = existing_game
            else:
                # Create new game
                game = crud.create_game(db, schemas.GameCreate(**game_info))
            
            print(f"Generating projections for {game_info['away_team']} @ {game_info['home_team']}...")
            
            # Generate player projections
            projections = stats_service.generate_projections_for_game(game_data)
            
            print(f"Generated {len(projections)} projections")
            
            # Add projections to database
            for proj_data in projections:
                proj_data['game_id'] = game.id
                crud.create_player_prop(db, schemas.PlayerPropCreate(**proj_data))
            
            updated_count += 1
        
        return {
            "message": "Projections updated successfully",
            "updated": updated_count,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    except Exception as e:
        print(f"Error updating projections: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error updating projections: {str(e)}")

@app.get("/api/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}