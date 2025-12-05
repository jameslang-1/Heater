# app/models.py
from sqlalchemy import Column, Integer, String, DateTime, Numeric, ForeignKey, Index
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Game(Base):
    __tablename__ = "games"
    
    id = Column(Integer, primary_key=True, index=True)
    external_id = Column(String(255), unique=True, index=True)
    home_team = Column(String(100), nullable=False)
    away_team = Column(String(100), nullable=False)
    commence_time = Column(DateTime, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    player_props = relationship("PlayerProp", back_populates="game", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Game {self.away_team} @ {self.home_team}>"


class PlayerProp(Base):
    __tablename__ = "player_props"
    
    id = Column(Integer, primary_key=True, index=True)
    game_id = Column(Integer, ForeignKey("games.id"), nullable=False)
    player_name = Column(String(255), nullable=False, index=True)
    prop_type = Column(String(50), nullable=False)  # 'points', 'rebounds', 'assists'
    line = Column(Numeric(5, 1), nullable=False)
    over_odds = Column(Integer, nullable=False)  # American odds format
    under_odds = Column(Integer, nullable=False)
    bookmaker = Column(String(100), nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    game = relationship("Game", back_populates="player_props")
    
    # Composite index for efficient queries
    __table_args__ = (
        Index('idx_player_prop_type', 'player_name', 'prop_type'),
    )
    
    def __repr__(self):
        return f"<PlayerProp {self.player_name} {self.prop_type} {self.line}>"