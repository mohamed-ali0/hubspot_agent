"""
Database connection and session management
"""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, sessionmaker

class Base(DeclarativeBase):
    """Base class for all database models"""
    pass

# Initialize SQLAlchemy
db = SQLAlchemy(model_class=Base)

def get_db():
    """Get database instance"""
    return db

def create_session():
    """Create a new database session"""
    return db.session
