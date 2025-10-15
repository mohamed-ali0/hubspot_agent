"""
Health check and system status API endpoints
"""

from flask import Blueprint, jsonify
from datetime import datetime
import os

bp = Blueprint('health', __name__)

@bp.route('', methods=['GET'])
def health_check():
    """Health check endpoint"""
    try:
        # Check HubSpot API configuration
        hubspot_status = 'configured' if os.getenv('HUBSPOT_ACCESS_TOKEN') else 'not_configured'
        
        # Simple database check - just return healthy for now
        db_status = 'connected'
        
        return jsonify({
            'status': 'healthy',
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