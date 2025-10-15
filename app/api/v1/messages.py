"""
Message management API endpoints
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

bp = Blueprint('messages', __name__)

@bp.route('', methods=['GET'])
@jwt_required()
def get_messages():
    """Get all messages"""
    return jsonify({
        'messages': [],
        'total': 0,
        'message': 'Messages endpoint working'
    }), 200