"""
Session management API endpoints
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

bp = Blueprint('sessions', __name__)

@bp.route('', methods=['GET'])
@jwt_required()
def get_sessions():
    """Get all sessions"""
    return jsonify({
        'sessions': [],
        'total': 0,
        'message': 'Sessions endpoint working'
    }), 200