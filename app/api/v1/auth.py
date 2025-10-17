"""
Authentication API endpoints
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.models import User
from app.db.database import db
from app.core.security import SecurityService
from marshmallow import Schema, fields, ValidationError

bp = Blueprint('auth', __name__)

class LoginSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)

login_schema = LoginSchema()

@bp.route('/login', methods=['POST'])
def login():
    """Login endpoint"""
    try:
        # Validate request data
        data = login_schema.load(request.get_json())
        
        # Find user by username
        user = User.query.filter_by(username=data['username']).first()
        
        if not user or not user.verify_password(data['password']):
            return jsonify({'error': 'Invalid credentials'}), 401
        
        if not user.is_active:
            return jsonify({'error': 'Account is deactivated'}), 401
        
        # Create JWT token
        access_token = create_access_token(identity=user.id)
        
        return jsonify({
            'token': access_token,
            'user': {
                'id': user.id,
                'name': user.name,
                'username': user.username,
                'phone_number': user.phone_number,
                'email': user.email,
                'is_active': user.is_active
            }
        }), 200
        
    except ValidationError as e:
        return jsonify({'error': 'Validation error', 'details': e.messages}), 400
    except Exception as e:
        return jsonify({'error': 'Login failed', 'details': str(e)}), 500

@bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """Logout endpoint"""
    # In a real implementation, you might want to blacklist the token
    return jsonify({'message': 'Logged out successfully'}), 200

@bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """Get current user info"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({
            'id': user.id,
            'name': user.name,
            'username': user.username,
            'phone_number': user.phone_number,
            'email': user.email,
            'is_active': user.is_active,
            'created_at': user.created_at.isoformat() if user.created_at else None
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to get user info'}), 500