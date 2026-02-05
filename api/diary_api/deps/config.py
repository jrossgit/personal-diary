from typing import Annotated
from fastapi import Depends
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    cors_allowed_origins: list[str] = [
        "http://localhost:5714",    # Default port for local front-end
    ]
    
    sql_database: str = "sqlite:///./testdb.db"


def get_settings() -> Settings:
    return Settings()


SettingsDep = Annotated[Settings, Depends(get_settings)]
