"""
Log management API endpoints
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Log
from app.db.database import db

bp = Blueprint('logs', __name__)

@bp.route('', methods=['GET'])
@jwt_required()
def get_logs():
    """Get all logs"""
    try:
        current_user_id = get_jwt_identity()
        session_id = request.args.get('session_id', type=int)
        
        # Build query
        query = Log.query.filter_by(user_id=current_user_id)
        if session_id:
            query = query.filter_by(session_id=session_id)
        
        # Get logs
        logs = query.order_by(Log.created_at.desc()).all()
        
        # Convert to dict
        logs_data = [log.to_dict() for log in logs]
        
        return jsonify({
            'logs': logs_data,
            'total': len(logs_data),
            'message': f'Found {len(logs_data)} logs'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500