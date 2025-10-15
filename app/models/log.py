"""
Log model for HubSpot activities
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import db

class Log(db.Model):
    """Log model for HubSpot activities"""
    __tablename__ = 'logs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    session_id = Column(Integer, ForeignKey('chat_sessions.id'), nullable=False)
    chat_message_id = Column(Integer, ForeignKey('chat_messages.id'), nullable=False)

    # Log details
    log_type = Column(String(50), nullable=False)  # contact_action, deal, note, task, communication, call_meeting, association
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # HubSpot integration
    hubspot_id = Column(String(100), nullable=True)  # HubSpot record ID
    sync_status = Column(String(20), default='pending', nullable=False)  # pending, synced, failed
    sync_error = Column(Text, nullable=True)
    synced_at = Column(DateTime, nullable=True)

    # Relationships
    user = relationship('User', backref='logs')
    session = relationship('ChatSession', back_populates='logs')
    message = relationship('ChatMessage', back_populates='logs')

    def mark_as_synced(self, hubspot_id):
        """Mark log as synced with HubSpot"""
        self.sync_status = 'synced'
        self.hubspot_id = hubspot_id
        self.synced_at = datetime.utcnow()
        self.sync_error = None

    def mark_as_failed(self, error_message):
        """Mark log as failed"""
        self.sync_status = 'failed'
        self.sync_error = error_message

    def retry_sync(self):
        """Reset for retry"""
        self.sync_status = 'pending'
        self.sync_error = None
        self.synced_at = None

    def to_dict(self):
        """Convert log to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'session_id': self.session_id,
            'chat_message_id': self.chat_message_id,
            'log_type': self.log_type,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'hubspot_id': self.hubspot_id,
            'sync_status': self.sync_status,
            'sync_error': self.sync_error,
            'synced_at': self.synced_at.isoformat() if self.synced_at else None,
            'message': self.message.to_dict() if self.message else None
        }

    def __repr__(self):
        return f'<Log {self.id} - {self.log_type}>'
