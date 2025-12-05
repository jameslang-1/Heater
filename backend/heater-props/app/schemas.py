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


# PICK SCHEMAS - NEW
class PickBase(BaseModel):
    player_prop_id: int
    selection: str  # 'over' or 'under'
    line: float
    user_id: Optional[int] = None
    confidence: Optional[str] = None

class PickCreate(PickBase):
    pass

class PickResponse(PickBase):
    id: int
    created_at: datetime
    
    # Grading fields
    result: Optional[str] = None  # 'won', 'lost', 'push'
    actual_value: Optional[float] = None
    graded_at: Optional[datetime] = None
    
    # Include related prop info
    player_prop: Optional[PlayerPropResponse] = None
    
    class Config:
        from_attributes = True


class PickListResponse(BaseModel):
    picks: List[PickResponse]
    total: int


class UserRecordResponse(BaseModel):
    user_id: int
    record: dict  # {'won': int, 'lost': int, 'push': int, 'total': int}
    win_percentage: float
    pending: int


class LeaderboardEntry(BaseModel):
    user_id: int
    won: int
    lost: int
    push: int
    total: int
    win_percentage: float


class LeaderboardResponse(BaseModel):
    leaderboard: List[LeaderboardEntry]