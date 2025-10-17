"""
Chat session model
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import db

class ChatSession(db.Model):
    """Chat session model"""
    __tablename__ = 'chat_sessions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    started_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    ended_at = Column(DateTime, nullable=True)
    status = Column(String(20), default='active', nullable=False)  # active, closed
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    user = relationship('User', backref='sessions')
    messages = relationship('ChatMessage', back_populates='session', cascade='all, delete-orphan')
    logs = relationship('Log', back_populates='session', cascade='all, delete-orphan')

    @property
    def message_count(self):
        """Get message count"""
        return len(self.messages)

    @property
    def log_count(self):
        """Get log count"""
        return len(self.logs)

    @property
    def duration_minutes(self):
        """Get session duration in minutes"""
        end_time = self.ended_at if self.ended_at else datetime.utcnow()
        duration = end_time - self.started_at
        return int(duration.total_seconds() / 60)

    def close_session(self):
        """Close the session"""
        self.status = 'closed'
        self.ended_at = datetime.utcnow()

    def to_dict(self):
        """Convert session to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'ended_at': self.ended_at.isoformat() if self.ended_at else None,
            'status': self.status,
            'message_count': self.message_count,
            'log_count': self.log_count,
            'duration_minutes': self.duration_minutes
        }

    def __repr__(self):
        return f'<ChatSession {self.id} - {self.status}>'
