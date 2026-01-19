from typing import Annotated
from diary_api.deps.config import SettingsDep
from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session


def get_db(settings: SettingsDep):
    """
    Dependancy function to provide the database session class
    """
    engine = create_engine(settings.sql_database)
    session = sessionmaker(autocommit=False, autoflush=False, bind=engine)()
    try:
        yield session
    finally:
        session.close()


DBSession = Annotated[Session, Depends(get_db)]
