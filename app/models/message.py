"""
Chat message model
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import db

class ChatMessage(db.Model):
    """Chat message model"""
    __tablename__ = 'chat_messages'

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(Integer, ForeignKey('chat_sessions.id'), nullable=False)
    message_text = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    forwarded_from = Column(String(100), nullable=True)  # Phone number or contact name
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    session = relationship('ChatSession', back_populates='messages')
    logs = relationship('Log', back_populates='message', cascade='all, delete-orphan')

    @property
    def has_logs(self):
        """Check if message has associated logs"""
        return len(self.logs) > 0

    @property
    def log_count(self):
        """Get log count"""
        return len(self.logs)

    def to_dict(self):
        """Convert message to dictionary"""
        return {
            'id': self.id,
            'session_id': self.session_id,
            'message_text': self.message_text,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'forwarded_from': self.forwarded_from,
            'has_logs': self.has_logs,
            'log_count': self.log_count,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

    def __repr__(self):
        return f'<ChatMessage {self.id}>'
