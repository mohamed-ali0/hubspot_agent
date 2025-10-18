"""
HubSpot Contacts API - Complete CRUD operations with logging
"""

from flask import Blueprint, request, jsonify
from app.services.hubspot_service import HubSpotService
from app.models import User, Log, ChatSession, ChatMessage
from app.db.database import db
from marshmallow import Schema, fields, ValidationError
import json
from datetime import datetime
import jwt
from flask import current_app

bp = Blueprint('hubspot_contacts', __name__)

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
class ContactCreateSchema(Schema):
    token = fields.Str(required=True)
    session_id = fields.Int(required=True)
    chat_message_id = fields.Int(required=True)
    properties = fields.Raw(required=True)  # Accept both Dict and string

class ContactUpdateSchema(Schema):
    token = fields.Str(required=True)
    contact_id = fields.Str(required=True)
    session_id = fields.Int(required=True)
    chat_message_id = fields.Int(required=True)
    properties = fields.Raw(required=True)  # Accept both Dict and string

class ContactSearchSchema(Schema):
    token = fields.Str(required=True)
    session_id = fields.Int(required=True)
    chat_message_id = fields.Int(required=True)
    search_term = fields.Str(required=True)
    limit = fields.Int(missing=10)

class ContactGetSchema(Schema):
    token = fields.Str(required=True)
    session_id = fields.Int(required=True)
    chat_message_id = fields.Int(required=True)
    limit = fields.Int(missing=10)
    properties = fields.Raw(missing=[])  # Accept both list and string

class ContactGetByIdSchema(Schema):
    token = fields.Str(required=True)
    contact_id = fields.Str(required=True)
    session_id = fields.Int(required=True)
    chat_message_id = fields.Int(required=True)

class ContactDeleteSchema(Schema):
    token = fields.Str(required=True)
    contact_id = fields.Str(required=True)
    session_id = fields.Int(required=True)
    chat_message_id = fields.Int(required=True)

# Initialize schemas
contact_create_schema = ContactCreateSchema()
contact_update_schema = ContactUpdateSchema()
contact_search_schema = ContactSearchSchema()
contact_get_schema = ContactGetSchema()
contact_get_by_id_schema = ContactGetByIdSchema()
contact_delete_schema = ContactDeleteSchema()

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

@bp.route('/contacts/get', methods=['POST'])
def get_contacts():
    """Get all contacts from HubSpot"""
    try:
        # Authenticate from body
        current_user_id, error_response, status_code = authenticate_from_body()
        if error_response:
            return error_response, status_code
        
        data = contact_get_schema.load(request.get_json())
        limit = data.get('limit', 10)
        properties = data.get('properties', [])
        
        # Get contacts from HubSpot
        result = HubSpotService.get_contacts(limit=limit, user_id=current_user_id, properties=properties)
        
        # Log the operation
        _create_log(
            user_id=current_user_id,
            session_id=0,  # No specific session for general queries
            message_id=0,  # No specific message for general queries
            log_type='contact_action',
            hubspot_id='multiple',
            sync_status='synced'
        )
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/contacts/get-by-id', methods=['POST'])
def get_contact():
    """Get specific contact by ID"""
    try:
        # Authenticate from body
        current_user_id, error_response, status_code = authenticate_from_body()
        if error_response:
            return error_response, status_code
        
        data = contact_get_by_id_schema.load(request.get_json())
        contact_id = data['contact_id']
        
        # Get contact from HubSpot
        result = HubSpotService.get_contact_by_id(contact_id, user_id=current_user_id)
        
        # Log the operation
        _create_log(
            user_id=current_user_id,
            session_id=data['session_id'],
            message_id=data['chat_message_id'],
            log_type='contact_action',
            hubspot_id=contact_id,
            sync_status='synced'
        )
        
        return jsonify(result), 200
        
    except ValidationError as e:
        return jsonify({'error': 'Validation error', 'details': e.messages}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/contacts/properties', methods=['POST'])
def get_contact_properties():
    """Get contact properties from HubSpot"""
    try:
        # Authenticate from body
        current_user_id, error_response, status_code = authenticate_from_body()
        if error_response:
            return error_response, status_code
        
        # Get contact properties from HubSpot
        result = HubSpotService.get_contact_properties(user_id=current_user_id)
        
        # Log the operation
        _create_log(
            user_id=current_user_id,
            session_id=0,
            message_id=0,
            log_type='contact_action',
            hubspot_id='properties',
            sync_status='synced'
        )
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/contacts/search', methods=['POST'])
def search_contacts():
    """Search contacts in HubSpot"""
    try:
        # Authenticate from body
        current_user_id, error_response, status_code = authenticate_from_body()
        if error_response:
            return error_response, status_code
        
        data = contact_search_schema.load(request.get_json())
        
        # Search contacts in HubSpot
        result = HubSpotService.search_contacts(
            search_term=data['search_term'],
            limit=data.get('limit', 10),
            user_id=current_user_id
        )
        
        # Log the operation
        _create_log(
            user_id=current_user_id,
            session_id=data['session_id'],
            message_id=data['chat_message_id'],
            log_type='contact_action',
            hubspot_id='search',
            sync_status='synced'
        )
        
        return jsonify(result), 200
        
    except ValidationError as e:
        return jsonify({'error': 'Validation error', 'details': e.messages}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ========== CREATE OPERATIONS ==========

@bp.route('/contacts', methods=['POST'])
def create_contact():
    """Create contact in HubSpot and log to database"""
    try:
        # Authenticate from body
        current_user_id, error_response, status_code = authenticate_from_body()
        if error_response:
            return error_response, status_code
        
        data = contact_create_schema.load(request.get_json())
        
        # Parse properties if it's a string
        properties = data['properties']
        if isinstance(properties, str):
            try:
                properties = json.loads(properties)
            except json.JSONDecodeError:
                return jsonify({'error': 'Invalid JSON in properties field'}), 400
        
        # Create contact in HubSpot
        result = HubSpotService.create_contact(
            contact_data=properties,
            session_id=data['session_id'],
            message_id=data['chat_message_id'],
            user_id=current_user_id
        )
        
        if result.get('success'):
            return jsonify({
                'message': 'Contact created successfully',
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

@bp.route('/contacts/update', methods=['POST'])
def update_contact():
    """Update contact in HubSpot and log to database"""
    try:
        # Authenticate from body
        current_user_id, error_response, status_code = authenticate_from_body()
        if error_response:
            return error_response, status_code
        
        data = contact_update_schema.load(request.get_json())
        contact_id = data['contact_id']
        
        # Parse properties if it's a string
        properties = data['properties']
        if isinstance(properties, str):
            try:
                properties = json.loads(properties)
            except json.JSONDecodeError:
                return jsonify({'error': 'Invalid JSON in properties field'}), 400
        
        # Update contact in HubSpot
        result = HubSpotService.update_contact(
            contact_id=contact_id,
            contact_data=properties,
            session_id=data['session_id'],
            message_id=data['chat_message_id'],
            user_id=current_user_id
        )
        
        if result.get('success'):
            return jsonify({
                'message': 'Contact updated successfully',
                'hubspot_id': contact_id,
                'data': result.get('data')
            }), 200
        else:
            return jsonify({'error': result.get('error')}), 400
            
    except ValidationError as e:
        return jsonify({'error': 'Validation error', 'details': e.messages}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/contacts/replace', methods=['POST'])
def replace_contact():
    """Replace contact in HubSpot and log to database"""
    try:
        # Authenticate from body
        current_user_id, error_response, status_code = authenticate_from_body()
        if error_response:
            return error_response, status_code
        
        data = contact_update_schema.load(request.get_json())
        contact_id = data['contact_id']
        
        # Parse properties if it's a string
        properties = data['properties']
        if isinstance(properties, str):
            try:
                properties = json.loads(properties)
            except json.JSONDecodeError:
                return jsonify({'error': 'Invalid JSON in properties field'}), 400
        
        # Replace contact in HubSpot
        result = HubSpotService.replace_contact(
            contact_id=contact_id,
            contact_data=properties,
            session_id=data['session_id'],
            message_id=data['chat_message_id'],
            user_id=current_user_id
        )
        
        if result.get('success'):
            return jsonify({
                'message': 'Contact replaced successfully',
                'hubspot_id': contact_id,
                'data': result.get('data')
            }), 200
        else:
            return jsonify({'error': result.get('error')}), 400
            
    except ValidationError as e:
        return jsonify({'error': 'Validation error', 'details': e.messages}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ========== DELETE OPERATIONS ==========

@bp.route('/contacts/delete', methods=['POST'])
def delete_contact():
    """Delete contact from HubSpot and log to database"""
    try:
        # Authenticate from body
        current_user_id, error_response, status_code = authenticate_from_body()
        if error_response:
            return error_response, status_code
        
        data = contact_delete_schema.load(request.get_json())
        contact_id = data['contact_id']
        
        # Delete contact from HubSpot
        result = HubSpotService.delete_contact(
            contact_id=contact_id,
            session_id=data['session_id'],
            message_id=data['chat_message_id'],
            user_id=current_user_id
        )
        
        if result.get('success'):
            return jsonify({
                'message': 'Contact deleted successfully',
                'hubspot_id': contact_id
            }), 200
        else:
            return jsonify({'error': result.get('error')}), 400
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ========== BATCH OPERATIONS ==========

@bp.route('/contacts/batch', methods=['POST'])
def batch_create_contacts():
    """Create multiple contacts in batch"""
    try:
        # Authenticate from body
        current_user_id, error_response, status_code = authenticate_from_body()
        if error_response:
            return error_response, status_code
        
        data = request.get_json()
        
        contacts_data = data.get('contacts', [])
        session_id = data.get('session_id', 0)
        message_id = data.get('chat_message_id', 0)
        
        # Batch create contacts
        result = HubSpotService.batch_create_contacts(
            contacts_data=contacts_data,
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

@bp.route('/contacts/batch/update', methods=['POST'])
def batch_update_contacts():
    """Update multiple contacts in batch"""
    try:
        # Authenticate from body
        current_user_id, error_response, status_code = authenticate_from_body()
        if error_response:
            return error_response, status_code
        
        data = request.get_json()
        
        contacts_data = data.get('contacts', [])
        session_id = data.get('session_id', 0)
        message_id = data.get('chat_message_id', 0)
        
        # Batch update contacts
        result = HubSpotService.batch_update_contacts(
            contacts_data=contacts_data,
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


@bp.route('/contacts/properties/get', methods=['POST'])
def get_contact_property():
    """Get specific contact property schema"""
    try:
        # Authenticate from body
        current_user_id, error_response, status_code = authenticate_from_body()
        if error_response:
            return error_response, status_code
        
        data = request.get_json()
        property_name = data.get('property_name')
        
        if not property_name:
            return jsonify({'error': 'property_name is required'}), 400
        
        # Get specific property from HubSpot
        result = HubSpotService.get_contact_property(property_name, user_id=current_user_id)
        
        # Log the operation
        _create_log(
            user_id=current_user_id,
            session_id=0,
            message_id=0,
            log_type='contact_action',
            hubspot_id=f'property_{property_name}',
            sync_status='synced'
        )
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
