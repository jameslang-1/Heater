# app/crud.py
from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import datetime, timedelta
from typing import List, Optional
from app import models, schemas

def create_game(db: Session, game: schemas.GameCreate) -> models.Game:
    """Create a new game"""
    db_game = models.Game(**game.dict())
    db.add(db_game)
    db.commit()
    db.refresh(db_game)
    return db_game

def get_game_by_external_id(db: Session, external_id: str) -> Optional[models.Game]:
    """Get game by external ID"""
    return db.query(models.Game).filter(models.Game.external_id == external_id).first()

def get_upcoming_games(db: Session, days_ahead: int = 14) -> List[models.Game]:
    """Get games in the next N days"""
    now = datetime.utcnow()
    future = now + timedelta(days=days_ahead)
    
    return db.query(models.Game).filter(
        and_(
            models.Game.commence_time >= now,
            models.Game.commence_time <= future
        )
    ).order_by(models.Game.commence_time).all()

def create_player_prop(db: Session, prop: schemas.PlayerPropCreate) -> models.PlayerProp:
    """Create a new player prop"""
    db_prop = models.PlayerProp(**prop.dict())
    db.add(db_prop)
    db.commit()
    db.refresh(db_prop)
    return db_prop

def delete_game_props(db: Session, game_id: int):
    """Delete all props for a game (before updating)"""
    db.query(models.PlayerProp).filter(models.PlayerProp.game_id == game_id).delete()
    db.commit()

def get_props_by_game(db: Session, game_id: int) -> List[models.PlayerProp]:
    """Get all props for a specific game"""
    return db.query(models.PlayerProp).filter(models.PlayerProp.game_id == game_id).all()

def get_props_by_player(db: Session, player_name: str, prop_type: Optional[str] = None) -> List[models.PlayerProp]:
    """Get props for a specific player, optionally filtered by prop type"""
    query = db.query(models.PlayerProp).filter(models.PlayerProp.player_name == player_name)
    
    if prop_type:
        query = query.filter(models.PlayerProp.prop_type == prop_type)
    
    return query.all()