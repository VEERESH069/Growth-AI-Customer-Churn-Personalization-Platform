from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from .models import Base

# Using SQLite for portability, but easily switchable to PostgreSQL
DATABASE_URL = "sqlite:///./growthai.db"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Initializes the database tables"""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created.")

def get_db():
    """Dependency for API sessions"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
