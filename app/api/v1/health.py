"""
Health check and system status API endpoints
"""

from flask import Blueprint, jsonify, current_app
from datetime import datetime

bp = Blueprint('health', __name__)

@bp.route('', methods=['GET'])
def health_check():
    """Health check endpoint - simplified version without model dependencies"""
    try:
        return jsonify({
            'status': 'healthy',
            'database': 'in_memory',
            'hubspot_api': 'available',
            'timestamp': datetime.utcnow().isoformat(),
            'message': 'HubSpot Logging AI Agent is running!',
            'version': '1.0.0',
            'environment': 'docker'
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