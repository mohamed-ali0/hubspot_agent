"""
HubSpot Contacts API - Complete CRUD operations with logging
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.hubspot_service import HubSpotService
from app.models import User, Log, ChatSession, ChatMessage
from app.db.database import db
from marshmallow import Schema, fields, ValidationError
from datetime import datetime

bp = Blueprint('hubspot_contacts', __name__)

# Request schemas
class ContactCreateSchema(Schema):
    session_id = fields.Int(required=True)
    chat_message_id = fields.Int(required=True)
    properties = fields.Dict(required=True)

class ContactUpdateSchema(Schema):
    session_id = fields.Int(required=True)
    chat_message_id = fields.Int(required=True)
    properties = fields.Dict(required=True)

class ContactSearchSchema(Schema):
    session_id = fields.Int(required=True)
    chat_message_id = fields.Int(required=True)
    search_term = fields.Str(required=True)

# Initialize schemas
contact_create_schema = ContactCreateSchema()
contact_update_schema = ContactUpdateSchema()
contact_search_schema = ContactSearchSchema()

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

@bp.route('/contacts', methods=['GET'])
@jwt_required()
def get_contacts():
    """Get all contacts from HubSpot"""
    try:
        current_user_id = get_jwt_identity()
        limit = request.args.get('limit', 10, type=int)
        properties = request.args.getlist('properties')
        
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

@bp.route('/contacts/<contact_id>', methods=['GET'])
@jwt_required()
def get_contact(contact_id):
    """Get specific contact by ID"""
    try:
        current_user_id = get_jwt_identity()
        
        # Get contact from HubSpot
        result = HubSpotService.get_contact_by_id(contact_id)
        
        # Log the operation
        _create_log(
            user_id=current_user_id,
            session_id=0,
            message_id=0,
            log_type='contact_action',
            hubspot_id=contact_id,
            sync_status='synced'
        )
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/properties', methods=['GET'])
@jwt_required()
def get_contact_properties():
    """Get contact properties from HubSpot"""
    try:
        current_user_id = get_jwt_identity()
        
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
@jwt_required()
def search_contacts():
    """Search contacts in HubSpot"""
    try:
        current_user_id = get_jwt_identity()
        data = contact_search_schema.load(request.get_json())
        
        # Search contacts in HubSpot
        result = HubSpotService.search_contacts(
            search_term=data['search_term'],
            limit=request.args.get('limit', 10, type=int)
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
@jwt_required()
def create_contact():
    """Create contact in HubSpot and log to database"""
    try:
        current_user_id = get_jwt_identity()
        data = contact_create_schema.load(request.get_json())
        
        # Create contact in HubSpot
        result = HubSpotService.create_contact(
            contact_data=data['properties'],
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

@bp.route('/contacts/<contact_id>', methods=['PATCH'])
@jwt_required()
def update_contact(contact_id):
    """Update contact in HubSpot and log to database"""
    try:
        current_user_id = get_jwt_identity()
        data = contact_update_schema.load(request.get_json())
        
        # Update contact in HubSpot
        result = HubSpotService.update_contact(
            contact_id=contact_id,
            contact_data=data['properties'],
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

@bp.route('/contacts/<contact_id>', methods=['PUT'])
@jwt_required()
def replace_contact(contact_id):
    """Replace contact in HubSpot and log to database"""
    try:
        current_user_id = get_jwt_identity()
        data = contact_update_schema.load(request.get_json())
        
        # Replace contact in HubSpot
        result = HubSpotService.replace_contact(
            contact_id=contact_id,
            contact_data=data['properties'],
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

@bp.route('/contacts/<contact_id>', methods=['DELETE'])
@jwt_required()
def delete_contact(contact_id):
    """Delete contact from HubSpot and log to database"""
    try:
        current_user_id = get_jwt_identity()
        session_id = request.json.get('session_id', 0) if request.is_json else 0
        message_id = request.json.get('chat_message_id', 0) if request.is_json else 0
        
        # Delete contact from HubSpot
        result = HubSpotService.delete_contact(
            contact_id=contact_id,
            session_id=session_id,
            message_id=message_id,
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
@jwt_required()
def batch_create_contacts():
    """Create multiple contacts in batch"""
    try:
        current_user_id = get_jwt_identity()
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

@bp.route('/contacts/batch', methods=['PATCH'])
@jwt_required()
def batch_update_contacts():
    """Update multiple contacts in batch"""
    try:
        current_user_id = get_jwt_identity()
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


@bp.route('/contacts/properties/<property_name>', methods=['GET'])
@jwt_required()
def get_contact_property(property_name):
    """Get specific contact property schema"""
    try:
        current_user_id = get_jwt_identity()
        
        # Get specific property from HubSpot
        result = HubSpotService.get_contact_property(property_name)
        
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
