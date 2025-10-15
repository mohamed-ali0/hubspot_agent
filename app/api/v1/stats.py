"""
Analytics and statistics API endpoints
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

bp = Blueprint('stats', __name__)

@bp.route('/overview', methods=['GET'])
@jwt_required()
def get_overview():
    """Get overview statistics"""
    return jsonify({
        'total_sessions': 0,
        'total_messages': 0,
        'total_logs': 0,
        'message': 'Stats endpoint working'
    }), 200