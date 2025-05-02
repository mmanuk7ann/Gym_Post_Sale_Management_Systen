"""
database.py

Configures SQLAlchemy for the Gym Project. This script:
- Loads environment variables from a `.env` file
- Initializes the database engine using the provided DATABASE_URL
- Defines a base class for models
- Creates a session factory for database operations
"""

import sqlalchemy as sql
import sqlalchemy.ext.declarative as declarative
import sqlalchemy.orm as orm
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv(".env")

# Get the database URL from environment variables
DATABASE_URL = os.environ.get("DATABASE_URL")

# Create the SQLAlchemy engine
engine = sql.create_engine(DATABASE_URL)

# Base class for declarative models
Base = declarative.declarative_base()

# SessionLocal for database operations
SessionLocal = orm.sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """
    Provides a SQLAlchemy database session.

    This is typically used as a FastAPI dependency to manage 
    opening and closing database sessions during request handling.

    Yields:
        Session: A SQLAlchemy database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
