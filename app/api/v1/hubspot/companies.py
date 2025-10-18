"""
HubSpot Companies API - Complete CRUD operations with logging
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from app.services.hubspot_service import HubSpotService
from app.models import User, Log, ChatSession, ChatMessage
from app.db.database import db
from marshmallow import Schema, fields, ValidationError
import json
from datetime import datetime
import jwt
from flask import current_app

bp = Blueprint('hubspot_companies', __name__)

def authenticate_from_body():
    """Authenticate user from token in request body"""
    try:
        # Get token from request body
        if request.is_json:
            token = request.json.get('token')
        else:
            token = request.form.get('token')
        
        if not token:
            return None, jsonify({'error': 'Token is required in request body'}), 401
        
        # Decode JWT token directly
        try:
            # Get the secret key from Flask app config
            secret_key = current_app.config.get('JWT_SECRET_KEY')
            if not secret_key:
                return None, jsonify({'error': 'JWT secret key not configured'}), 500
            
            # Decode the token
            decoded_token = jwt.decode(token, secret_key, algorithms=['HS256'])
            user_id = decoded_token.get('sub')  # 'sub' is the user ID in JWT
            
            if not user_id:
                return None, jsonify({'error': 'Invalid token: no user ID found'}), 401
            
            return user_id, None, None
            
        except jwt.ExpiredSignatureError:
            return None, jsonify({'error': 'Token has expired'}), 401
        except jwt.InvalidTokenError as e:
            return None, jsonify({'error': f'Invalid token: {str(e)}'}), 401
            
    except Exception as e:
        return None, jsonify({'error': f'Authentication error: {str(e)}'}), 401

# Request schemas
class CompanyCreateSchema(Schema):
    token = fields.Str(required=True)
    session_id = fields.Int(required=True)
    chat_message_id = fields.Int(required=True)
    properties = fields.Raw(required=True)  # Accept both Dict and string

class CompanyUpdateSchema(Schema):
    token = fields.Str(required=True)
    company_id = fields.Str(required=True)
    session_id = fields.Int(required=True)
    chat_message_id = fields.Int(required=True)
    properties = fields.Raw(required=True)  # Accept both Dict and string

class CompanySearchSchema(Schema):
    token = fields.Str(required=True)
    session_id = fields.Int(required=True)
    chat_message_id = fields.Int(required=True)
    search_term = fields.Str(required=True)

class CompanyGetSchema(Schema):
    token = fields.Str(required=True)
    limit = fields.Int(missing=10)
    properties = fields.List(fields.Str(), missing=[])

class CompanyGetByIdSchema(Schema):
    token = fields.Str(required=True)
    company_id = fields.Str(required=True)

class CompanySearchSchema(Schema):
    token = fields.Str(required=True)
    session_id = fields.Int(required=True)
    chat_message_id = fields.Int(required=True)
    search_term = fields.Str(required=True)
    limit = fields.Int(missing=10)

class CompanyDeleteSchema(Schema):
    token = fields.Str(required=True)
    company_id = fields.Str(required=True)
    session_id = fields.Int(missing=0)
    chat_message_id = fields.Int(missing=0)

# Initialize schemas
company_create_schema = CompanyCreateSchema()
company_update_schema = CompanyUpdateSchema()
company_search_schema = CompanySearchSchema()
company_get_schema = CompanyGetSchema()
company_get_by_id_schema = CompanyGetByIdSchema()
company_delete_schema = CompanyDeleteSchema()

def _create_log(user_id, session_id, message_id, log_type, hubspot_id, sync_status, sync_error=None):
    """Create a log entry for HubSpot operations"""
    try:
        log = Log(
            user_id=user_id,
            session_id=session_id,
            chat_message_id=message_id,
            log_type=log_type,
            hubspot_id=hubspot_id,
            sync_status=sync_status,
            sync_error=sync_error,
            synced_at=datetime.utcnow() if sync_status == 'synced' else None
        )
        db.session.add(log)
        db.session.commit()
        return log
    except Exception as e:
        db.session.rollback()
        return None

# ========== GET OPERATIONS ==========

@bp.route('/companies', methods=['GET'])
def get_companies():
    """Get all companies from HubSpot"""
    try:
        # Authenticate from body
        current_user_id, error_response, status_code = authenticate_from_body()
        if error_response:
            return error_response, status_code
        
        # Validate request body
        data = company_get_schema.load(request.get_json())
        
        # Get parameters from body instead of query
        limit = data.get('limit', 10)
        properties = data.get('properties', [])
        
        # Get companies from HubSpot
        result = HubSpotService.get_companies(limit=limit, user_id=current_user_id, properties=properties)
        
        # Log the operation
        _create_log(
            user_id=current_user_id,
            session_id=0,
            message_id=0,
            log_type='company_action',
            hubspot_id='multiple',
            sync_status='synced'
        )
        
        return jsonify(result), 200
        
    except ValidationError as e:
        return jsonify({'error': 'Validation error', 'details': e.messages}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/companies/get', methods=['POST'])
def get_company():
    """Get specific company by ID"""
    try:
        # Authenticate from body
        current_user_id, error_response, status_code = authenticate_from_body()
        if error_response:
            return error_response, status_code
        
        # Validate request body
        data = company_get_by_id_schema.load(request.get_json())
        company_id = data['company_id']
        
        # Get company from HubSpot
        result = HubSpotService.get_company_by_id(company_id, user_id=current_user_id)
        
        # Log the operation
        _create_log(
            user_id=current_user_id,
            session_id=0,
            message_id=0,
            log_type='company_action',
            hubspot_id=company_id,
            sync_status='synced'
        )
        
        return jsonify(result), 200
        
    except ValidationError as e:
        return jsonify({'error': 'Validation error', 'details': e.messages}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/properties', methods=['GET'])
def get_company_properties():
    """Get company properties from HubSpot"""
    try:
        # Authenticate from body
        current_user_id, error_response, status_code = authenticate_from_body()
        if error_response:
            return error_response, status_code
        
        # Validate request body
        data = company_get_schema.load(request.get_json())
        
        # Get company properties from HubSpot
        result = HubSpotService.get_company_properties(user_id=current_user_id)
        
        # Log the operation
        _create_log(
            user_id=current_user_id,
            session_id=0,
            message_id=0,
            log_type='company_action',
            hubspot_id='properties',
            sync_status='synced'
        )
        
        return jsonify(result), 200
        
    except ValidationError as e:
        return jsonify({'error': 'Validation error', 'details': e.messages}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/companies/search', methods=['POST'])
def search_companies():
    """Search companies in HubSpot"""
    try:
        # Authenticate from body
        current_user_id, error_response, status_code = authenticate_from_body()
        if error_response:
            return error_response, status_code
        
        data = company_search_schema.load(request.get_json())
        
        # Search companies in HubSpot using body parameters
        result = HubSpotService.search_companies(
            search_term=data['search_term'],
            limit=data.get('limit', 10),
            user_id=current_user_id
        )
        
        # Log the operation
        _create_log(
            user_id=current_user_id,
            session_id=data['session_id'],
            message_id=data['chat_message_id'],
            log_type='company_action',
            hubspot_id='search',
            sync_status='synced'
        )
        
        return jsonify(result), 200
        
    except ValidationError as e:
        return jsonify({'error': 'Validation error', 'details': e.messages}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ========== CREATE OPERATIONS ==========

@bp.route('/companies', methods=['POST'])
def create_company():
    """Create company in HubSpot and log to database"""
    try:
        # Authenticate from body
        current_user_id, error_response, status_code = authenticate_from_body()
        if error_response:
            return error_response, status_code
        
        data = company_create_schema.load(request.get_json())
        
        # Parse properties if it's a string
        properties = data['properties']
        if isinstance(properties, str):
            try:
                properties = json.loads(properties)
            except json.JSONDecodeError:
                return jsonify({'error': 'Invalid JSON in properties field'}), 400
        
        # Create company in HubSpot
        result = HubSpotService.create_company(
            company_data=properties,
            session_id=data['session_id'],
            message_id=data['chat_message_id'],
            user_id=current_user_id
        )
        
        if result.get('success'):
            return jsonify({
                'message': 'Company created successfully',
                'hubspot_id': result.get('hubspot_id'),
                'data': result.get('data')
            }), 201
        else:
            return jsonify({'error': result.get('error')}), 400
            
    except ValidationError as e:
        return jsonify({'error': 'Validation error', 'details': e.messages}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ========== UPDATE OPERATIONS ==========

@bp.route('/companies/update', methods=['POST'])
def update_company():
    """Update company in HubSpot and log to database"""
    try:
        # Authenticate from body
        current_user_id, error_response, status_code = authenticate_from_body()
        if error_response:
            return error_response, status_code
        
        data = company_update_schema.load(request.get_json())
        company_id = data['company_id']
        
        # Parse properties if it's a string
        properties = data['properties']
        if isinstance(properties, str):
            try:
                properties = json.loads(properties)
            except json.JSONDecodeError:
                return jsonify({'error': 'Invalid JSON in properties field'}), 400
        
        # Update company in HubSpot
        result = HubSpotService.update_company(
            company_id=company_id,
            company_data=properties,
            session_id=data['session_id'],
            message_id=data['chat_message_id'],
            user_id=current_user_id
        )
        
        if result.get('success'):
            return jsonify({
                'message': 'Company updated successfully',
                'hubspot_id': company_id,
                'data': result.get('data')
            }), 200
        else:
            return jsonify({'error': result.get('error')}), 400
            
    except ValidationError as e:
        return jsonify({'error': 'Validation error', 'details': e.messages}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/companies/replace', methods=['POST'])
def replace_company():
    """Replace company in HubSpot and log to database"""
    try:
        # Authenticate from body
        current_user_id, error_response, status_code = authenticate_from_body()
        if error_response:
            return error_response, status_code
        
        data = company_update_schema.load(request.get_json())
        company_id = data['company_id']
        
        # Replace company in HubSpot
        result = HubSpotService.replace_company(
            company_id=company_id,
            company_data=data['properties'],
            session_id=data['session_id'],
            message_id=data['chat_message_id'],
            user_id=current_user_id
        )
        
        if result.get('success'):
            return jsonify({
                'message': 'Company replaced successfully',
                'hubspot_id': company_id,
                'data': result.get('data')
            }), 200
        else:
            return jsonify({'error': result.get('error')}), 400
            
    except ValidationError as e:
        return jsonify({'error': 'Validation error', 'details': e.messages}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ========== DELETE OPERATIONS ==========

@bp.route('/companies/delete', methods=['POST'])
def delete_company():
    """Delete company from HubSpot and log to database"""
    try:
        # Authenticate from body
        current_user_id, error_response, status_code = authenticate_from_body()
        if error_response:
            return error_response, status_code
        
        # Validate request body
        data = company_delete_schema.load(request.get_json())
        company_id = data['company_id']
        
        # Delete company from HubSpot
        result = HubSpotService.delete_company(
            company_id=company_id,
            session_id=data.get('session_id', 0),
            message_id=data.get('chat_message_id', 0),
            user_id=current_user_id
        )
        
        if result.get('success'):
            return jsonify({
                'message': 'Company deleted successfully',
                'hubspot_id': company_id
            }), 200
        else:
            return jsonify({'error': result.get('error')}), 400
            
    except ValidationError as e:
        return jsonify({'error': 'Validation error', 'details': e.messages}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ========== BATCH OPERATIONS ==========

@bp.route('/companies/batch', methods=['POST'])
def batch_create_companies():
    """Create multiple companies in batch"""
    try:
        # Authenticate from body
        current_user_id, error_response, status_code = authenticate_from_body()
        if error_response:
            return error_response, status_code
        
        data = request.get_json()
        
        companies_data = data.get('companies', [])
        session_id = data.get('session_id', 0)
        message_id = data.get('chat_message_id', 0)
        
        # Batch create companies
        result = HubSpotService.batch_create_companies(
            companies_data=companies_data,
            session_id=session_id,
            message_id=message_id,
            user_id=current_user_id
        )
        
        return jsonify({
            'message': f'Batch operation completed',
            'results': result
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/companies/batch', methods=['PATCH'])
def batch_update_companies():
    """Update multiple companies in batch"""
    try:
        # Authenticate from body
        current_user_id, error_response, status_code = authenticate_from_body()
        if error_response:
            return error_response, status_code
        
        data = request.get_json()
        
        companies_data = data.get('companies', [])
        session_id = data.get('session_id', 0)
        message_id = data.get('chat_message_id', 0)
        
        # Batch update companies
        result = HubSpotService.batch_update_companies(
            companies_data=companies_data,
            session_id=session_id,
            message_id=message_id,
            user_id=current_user_id
        )
        
        return jsonify({
            'message': f'Batch update completed',
            'results': result
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ========== PROPERTIES OPERATIONS ==========


@bp.route('/companies/properties/get', methods=['POST'])
def get_company_property():
    """Get specific company property schema"""
    try:
        # Authenticate from body
        current_user_id, error_response, status_code = authenticate_from_body()
        if error_response:
            return error_response, status_code
        
        # Get property name from body
        data = request.get_json()
        property_name = data.get('property_name')
        
        if not property_name:
            return jsonify({'error': 'property_name is required in request body'}), 400
        
        # Get specific property from HubSpot
        result = HubSpotService.get_company_property(property_name)
        
        # Log the operation
        _create_log(
            user_id=current_user_id,
            session_id=0,
            message_id=0,
            log_type='company_action',
            hubspot_id=f'property_{property_name}',
            sync_status='synced'
        )
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
