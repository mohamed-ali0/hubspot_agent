"""
HubSpot integration API endpoints
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.hubspot_service import HubSpotService
from app.models import User, Log, ChatSession, ChatMessage
from app.db.database import db
from marshmallow import Schema, fields, ValidationError

bp = Blueprint('hubspot', __name__)

# Request schemas
class ContactCreateSchema(Schema):
    session_id = fields.Int(required=True)
    chat_message_id = fields.Int(required=True)
    properties = fields.Dict(required=True)

class DealCreateSchema(Schema):
    session_id = fields.Int(required=True)
    chat_message_id = fields.Int(required=True)
    properties = fields.Dict(required=True)
    associations = fields.Dict(missing={})

class NoteCreateSchema(Schema):
    session_id = fields.Int(required=True)
    chat_message_id = fields.Int(required=True)
    properties = fields.Dict(required=True)
    associations = fields.Dict(missing={})

class TaskCreateSchema(Schema):
    session_id = fields.Int(required=True)
    chat_message_id = fields.Int(required=True)
    properties = fields.Dict(required=True)
    associations = fields.Dict(missing={})

class EngagementCreateSchema(Schema):
    session_id = fields.Int(required=True)
    chat_message_id = fields.Int(required=True)
    engagement_type = fields.Str(required=True)
    properties = fields.Dict(required=True)
    associations = fields.Dict(missing={})

# Initialize schemas
contact_schema = ContactCreateSchema()
deal_schema = DealCreateSchema()
note_schema = NoteCreateSchema()
task_schema = TaskCreateSchema()
engagement_schema = EngagementCreateSchema()

@bp.route('/test-connection', methods=['GET'])
@jwt_required()
def test_connection():
    """Test HubSpot connection"""
    try:
        # Test basic connectivity
        result = HubSpotService.test_connection()
        return jsonify({
            'status': 'connected',
            'message': 'HubSpot connection successful',
            'details': result
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'HubSpot connection failed',
            'error': str(e)
        }), 500

@bp.route('/contacts', methods=['GET'])
@jwt_required()
def get_contacts():
    """Get contacts from HubSpot"""
    try:
        limit = request.args.get('limit', 10, type=int)
        result = HubSpotService.get_contacts(limit=limit)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/contacts', methods=['POST'])
@jwt_required()
def create_contact():
    """Create contact in HubSpot and log to database"""
    try:
        # Validate request data
        data = contact_schema.load(request.get_json())
        
        # Get current user
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Create contact in HubSpot
        hubspot_result = HubSpotService.create_contact(
            properties=data['properties']
        )
        
        # Log to database
        log = Log(
            user_id=user.id,
            session_id=data['session_id'],
            chat_message_id=data['chat_message_id'],
            log_type='contact_action',
            hubspot_id=hubspot_result.get('id'),
            sync_status='synced' if hubspot_result.get('id') else 'failed'
        )
        
        db.session.add(log)
        db.session.commit()
        
        return jsonify({
            'log_id': log.id,
            'hubspot_id': hubspot_result.get('id'),
            'sync_status': log.sync_status,
            'message': 'Contact created in HubSpot'
        }), 201
        
    except ValidationError as e:
        return jsonify({'error': 'Validation error', 'details': e.messages}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/deals', methods=['GET'])
@jwt_required()
def get_deals():
    """Get deals from HubSpot"""
    try:
        limit = request.args.get('limit', 10, type=int)
        result = HubSpotService.get_deals(limit=limit)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/deals', methods=['POST'])
@jwt_required()
def create_deal():
    """Create deal in HubSpot and log to database"""
    try:
        # Validate request data
        data = deal_schema.load(request.get_json())
        
        # Get current user
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Create deal in HubSpot
        hubspot_result = HubSpotService.create_deal(
            properties=data['properties'],
            associations=data.get('associations', {})
        )
        
        # Log to database
        log = Log(
            user_id=user.id,
            session_id=data['session_id'],
            chat_message_id=data['chat_message_id'],
            log_type='deal',
            hubspot_id=hubspot_result.get('id'),
            sync_status='synced' if hubspot_result.get('id') else 'failed'
        )
        
        db.session.add(log)
        db.session.commit()
        
        return jsonify({
            'log_id': log.id,
            'hubspot_id': hubspot_result.get('id'),
            'sync_status': log.sync_status,
            'message': 'Deal created in HubSpot'
        }), 201
        
    except ValidationError as e:
        return jsonify({'error': 'Validation error', 'details': e.messages}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/notes', methods=['GET'])
@jwt_required()
def get_notes():
    """Get notes from HubSpot"""
    try:
        limit = request.args.get('limit', 10, type=int)
        result = HubSpotService.get_notes(limit=limit)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/notes', methods=['POST'])
@jwt_required()
def create_note():
    """Create note in HubSpot and log to database"""
    try:
        # Validate request data
        data = note_schema.load(request.get_json())
        
        # Get current user
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Create note in HubSpot
        hubspot_result = HubSpotService.create_note(
            properties=data['properties'],
            associations=data.get('associations', {})
        )
        
        # Log to database
        log = Log(
            user_id=user.id,
            session_id=data['session_id'],
            chat_message_id=data['chat_message_id'],
            log_type='note',
            hubspot_id=hubspot_result.get('id'),
            sync_status='synced' if hubspot_result.get('id') else 'failed'
        )
        
        db.session.add(log)
        db.session.commit()
        
        return jsonify({
            'log_id': log.id,
            'hubspot_id': hubspot_result.get('id'),
            'sync_status': log.sync_status,
            'message': 'Note created in HubSpot'
        }), 201
        
    except ValidationError as e:
        return jsonify({'error': 'Validation error', 'details': e.messages}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/tasks', methods=['GET'])
@jwt_required()
def get_tasks():
    """Get tasks from HubSpot"""
    try:
        limit = request.args.get('limit', 10, type=int)
        result = HubSpotService.get_tasks(limit=limit)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/tasks', methods=['POST'])
@jwt_required()
def create_task():
    """Create task in HubSpot and log to database"""
    try:
        # Validate request data
        data = task_schema.load(request.get_json())
        
        # Get current user
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Create task in HubSpot
        hubspot_result = HubSpotService.create_task(
            properties=data['properties'],
            associations=data.get('associations', {})
        )
        
        # Log to database
        log = Log(
            user_id=user.id,
            session_id=data['session_id'],
            chat_message_id=data['chat_message_id'],
            log_type='task',
            hubspot_id=hubspot_result.get('id'),
            sync_status='synced' if hubspot_result.get('id') else 'failed'
        )
        
        db.session.add(log)
        db.session.commit()
        
        return jsonify({
            'log_id': log.id,
            'hubspot_id': hubspot_result.get('id'),
            'sync_status': log.sync_status,
            'message': 'Task created in HubSpot'
        }), 201
        
    except ValidationError as e:
        return jsonify({'error': 'Validation error', 'details': e.messages}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/meetings', methods=['GET'])
@jwt_required()
def get_meetings():
    """Get meetings from HubSpot"""
    try:
        limit = request.args.get('limit', 10, type=int)
        result = HubSpotService.get_meetings(limit=limit)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/meetings', methods=['POST'])
@jwt_required()
def create_meeting():
    """Create meeting in HubSpot and log to database"""
    try:
        # Validate request data
        data = engagement_schema.load(request.get_json())
        
        # Get current user
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Create meeting in HubSpot
        hubspot_result = HubSpotService.create_meeting(
            properties=data['properties'],
            associations=data.get('associations', {})
        )
        
        # Log to database
        log = Log(
            user_id=user.id,
            session_id=data['session_id'],
            chat_message_id=data['chat_message_id'],
            log_type='call_meeting',
            hubspot_id=hubspot_result.get('id'),
            sync_status='synced' if hubspot_result.get('id') else 'failed'
        )
        
        db.session.add(log)
        db.session.commit()
        
        return jsonify({
            'log_id': log.id,
            'hubspot_id': hubspot_result.get('id'),
            'sync_status': log.sync_status,
            'message': 'Meeting created in HubSpot'
        }), 201
        
    except ValidationError as e:
        return jsonify({'error': 'Validation error', 'details': e.messages}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/companies', methods=['GET'])
@jwt_required()
def get_companies():
    """Get companies from HubSpot"""
    try:
        limit = request.args.get('limit', 10, type=int)
        result = HubSpotService.get_companies(limit=limit)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/owners', methods=['GET'])
@jwt_required()
def get_owners():
    """Get owners from HubSpot"""
    try:
        limit = request.args.get('limit', 10, type=int)
        result = HubSpotService.get_owners(limit=limit)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500