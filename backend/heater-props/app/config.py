# app/config.py
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    database_url: str
    odds_api_key: str
    odds_api_base_url: str = "https://api.the-odds-api.com/v4"
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()