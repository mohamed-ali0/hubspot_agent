"""
Health check and system status API endpoints
"""

from flask import Blueprint, jsonify, current_app
from datetime import datetime
from app.models import User
from app.db.database import db
from sqlalchemy import text

bp = Blueprint('health', __name__)

@bp.route('', methods=['GET'])
def health_check():
    """Health check endpoint"""
    try:
        # Check database connection
        db_status = 'connected'
        try:
            db.session.execute(text('SELECT 1'))
        except Exception:
            db_status = 'error'

        # Check if any users have HubSpot tokens configured
        hubspot_status = 'not_configured'
        try:
            users_with_tokens = User.query.filter(User.hubspot_pat_token.isnot(None)).count()
            if users_with_tokens > 0:
                hubspot_status = 'configured'
        except Exception:
            hubspot_status = 'error'
        
        return jsonify({
            'status': 'healthy' if db_status == 'connected' else 'unhealthy',
            'database': db_status,
            'hubspot_api': hubspot_status,
            'timestamp': datetime.utcnow().isoformat(),
            'message': 'HubSpot Logging AI Agent is running!'
        }), 200

    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }), 500

@bp.route('/test', methods=['GET'])
def test_endpoint():
    """Simple test endpoint"""
    return jsonify({
        'message': 'Test endpoint working!',
        'timestamp': datetime.utcnow().isoformat()
    }), 200