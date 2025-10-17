"""
Custom authentication decorator for body-based JWT tokens
"""

from functools import wraps
from flask import request, jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity

def jwt_required_body():
    """
    Custom JWT decorator that reads token from request body instead of Authorization header
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                # Get token from request body
                if request.is_json:
                    token = request.json.get('token')
                else:
                    # Try to get from form data
                    token = request.form.get('token')
                
                if not token:
                    return jsonify({'error': 'Token is required in request body'}), 401
                
                # Create a temporary request with Authorization header for JWT verification
                original_headers = request.headers
                request.headers = request.headers.copy()
                request.headers['Authorization'] = f'Bearer {token}'
                
                try:
                    # Verify the JWT token
                    verify_jwt_in_request()
                    user_id = get_jwt_identity()
                    
                    # Store user_id in request context for easy access
                    request.user_id = user_id
                    
                    return f(*args, **kwargs)
                    
                except Exception as e:
                    return jsonify({'error': f'Invalid token: {str(e)}'}), 401
                    
                finally:
                    # Restore original headers
                    request.headers = original_headers
                    
            except Exception as e:
                return jsonify({'error': f'Authentication error: {str(e)}'}), 401
                
        return decorated_function
    return decorator

def get_current_user_id():
    """
    Get current user ID from request context
    """
    return getattr(request, 'user_id', None)
