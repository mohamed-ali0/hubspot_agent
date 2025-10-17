"""
Database models package
"""

# Global flag to prevent duplicate model imports
_models_imported = False

def import_models():
    """Import models only once to prevent SQLAlchemy conflicts"""
    global _models_imported
    if not _models_imported:
        from .user import User
        from .session import ChatSession
        from .message import ChatMessage
        from .log import Log
        _models_imported = True
        return User, ChatSession, ChatMessage, Log
    else:
        # Return already imported models
        from .user import User
        from .session import ChatSession
        from .message import ChatMessage
        from .log import Log
        return User, ChatSession, ChatMessage, Log

# Import models immediately
User, ChatSession, ChatMessage, Log = import_models()

__all__ = ['User', 'ChatSession', 'ChatMessage', 'Log']