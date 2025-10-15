from typing import Annotated
from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session


def get_db():
    """
    Dependancy function to provide the database session class
    """
    engine = create_engine("sqlite:///./testdb.db")
    session = sessionmaker(autocommit=False, autoflush=False, bind=engine)()
    try:
        yield session
    finally:
        session.close()


DBSession = Annotated[Session, Depends(get_db)]
