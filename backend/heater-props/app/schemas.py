# app/schemas.py
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class PlayerPropBase(BaseModel):
    player_name: str
    prop_type: str
    line: float
    over_odds: int
    under_odds: int
    bookmaker: str

class PlayerPropCreate(PlayerPropBase):
    game_id: int

class PlayerPropResponse(PlayerPropBase):
    id: int
    game_id: int
    updated_at: datetime
    
    class Config:
        from_attributes = True


class GameBase(BaseModel):
    external_id: str
    home_team: str
    away_team: str
    commence_time: datetime

class GameCreate(GameBase):
    pass

class GameResponse(GameBase):
    id: int
    created_at: datetime
    updated_at: datetime
    player_props: List[PlayerPropResponse] = []
    
    class Config:
        from_attributes = True


class GameListResponse(BaseModel):
    games: List[GameResponse]
    total: int