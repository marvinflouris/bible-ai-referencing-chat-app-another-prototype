"""
Database connection and session management
"""

from sqlmodel import SQLModel, create_engine, Session
from typing import Generator
from app.config import settings

# Create database engine
engine = create_engine(
    settings.DATABASE_URL,
    echo=False,  # Set to True to see SQL queries
    future=True
)

def init_db():
    """
    Create all tables in the database
    Call this once at startup
    """
    SQLModel.metadata.create_all(engine)
    print("✓ Database tables created/verified")

def get_session() -> Generator[Session, None, None]:
    """
    Dependency for getting database session
    Use this in FastAPI routes
    
    Example:
        @app.get("/verses")
        def get_verses(session: Session = Depends(get_session)):
            ...
    """
    with Session(engine) as session:
        yield session

def create_session() -> Session:
    """
    Create a single database session
    Use this for standalone scripts or CLI commands
    
    Example:
        session = create_session()
        verses = session.query(Verse).all()
        session.close()
    """
    return Session(engine)
