"""
HubSpot Activities API - Calls, Meetings, Visits with logging
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.hubspot_service import HubSpotService
from app.models import User, Log, ChatSession, ChatMessage
from app.db.database import db
from marshmallow import Schema, fields, ValidationError
from datetime import datetime

bp = Blueprint('hubspot_activities', __name__)

# Request schemas
class ActivityCreateSchema(Schema):
    session_id = fields.Int(required=True)
    chat_message_id = fields.Int(required=True)
    activity_type = fields.Str(required=True)  # CALL, MEETING, EMAIL, etc.
    properties = fields.Dict(required=True)
    associations = fields.Dict(missing={})

class ActivityUpdateSchema(Schema):
    session_id = fields.Int(required=True)
    chat_message_id = fields.Int(required=True)
    activity_type = fields.Str(required=True)
    properties = fields.Dict(required=True)
    associations = fields.Dict(missing={})

class ActivitySearchSchema(Schema):
    session_id = fields.Int(required=True)
    chat_message_id = fields.Int(required=True)
    activity_type = fields.Str(required=True)
    search_term = fields.Str(required=True)

# Initialize schemas
activity_create_schema = ActivityCreateSchema()
activity_update_schema = ActivityUpdateSchema()
activity_search_schema = ActivitySearchSchema()

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

# ========== CALL OPERATIONS ==========

@bp.route('/calls', methods=['GET'])
@jwt_required()
def get_calls():
    """Get all calls from HubSpot"""
    try:
        current_user_id = get_jwt_identity()
        limit = request.args.get('limit', 10, type=int)
        properties = request.args.getlist('properties')
        
        # Get calls from HubSpot
        result = HubSpotService.get_calls(limit=limit, user_id=current_user_id, properties=properties)
        
        # Log the operation
        _create_log(
            user_id=current_user_id,
            session_id=0,
            message_id=0,
            log_type='call_meeting',
            hubspot_id='multiple',
            sync_status='synced'
        )
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/calls/<call_id>', methods=['GET'])
@jwt_required()
def get_call(call_id):
    """Get specific call by ID"""
    try:
        current_user_id = get_jwt_identity()
        
        # Get call from HubSpot
        result = HubSpotService.get_call_by_id(call_id)
        
        # Log the operation
        _create_log(
            user_id=current_user_id,
            session_id=0,
            message_id=0,
            log_type='call_meeting',
            hubspot_id=call_id,
            sync_status='synced'
        )
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/calls', methods=['POST'])
@jwt_required()
def create_call():
    """Create call in HubSpot and log to database"""
    try:
        current_user_id = get_jwt_identity()
        data = activity_create_schema.load(request.get_json())
        
        # Create call in HubSpot
        result = HubSpotService.create_call(
            call_data=data['properties'],
            associations=data.get('associations', {}),
            session_id=data['session_id'],
            message_id=data['chat_message_id'],
            user_id=current_user_id
        )
        
        if result.get('success'):
            return jsonify({
                'message': 'Call created successfully',
                'hubspot_id': result.get('hubspot_id'),
                'data': result.get('data')
            }), 201
        else:
            return jsonify({'error': result.get('error')}), 400
            
    except ValidationError as e:
        return jsonify({'error': 'Validation error', 'details': e.messages}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ========== MEETING OPERATIONS ==========

@bp.route('/meetings', methods=['GET'])
@jwt_required()
def get_meetings():
    """Get all meetings from HubSpot"""
    try:
        current_user_id = get_jwt_identity()
        limit = request.args.get('limit', 10, type=int)
        properties = request.args.getlist('properties')
        
        # Get meetings from HubSpot
        result = HubSpotService.get_meetings(limit=limit, user_id=current_user_id, properties=properties)
        
        # Log the operation
        _create_log(
            user_id=current_user_id,
            session_id=0,
            message_id=0,
            log_type='call_meeting',
            hubspot_id='multiple',
            sync_status='synced'
        )
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/meetings/<meeting_id>', methods=['GET'])
@jwt_required()
def get_meeting(meeting_id):
    """Get specific meeting by ID"""
    try:
        current_user_id = get_jwt_identity()
        
        # Get meeting from HubSpot
        result = HubSpotService.get_meeting_by_id(meeting_id)
        
        # Log the operation
        _create_log(
            user_id=current_user_id,
            session_id=0,
            message_id=0,
            log_type='call_meeting',
            hubspot_id=meeting_id,
            sync_status='synced'
        )
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/meetings', methods=['POST'])
@jwt_required()
def create_meeting():
    """Create meeting in HubSpot and log to database"""
    try:
        current_user_id = get_jwt_identity()
        data = activity_create_schema.load(request.get_json())
        
        # Create meeting in HubSpot
        result = HubSpotService.create_meeting(
            meeting_data=data['properties'],
            associations=data.get('associations', {}),
            session_id=data['session_id'],
            message_id=data['chat_message_id'],
            user_id=current_user_id
        )
        
        if result.get('success'):
            return jsonify({
                'message': 'Meeting created successfully',
                'hubspot_id': result.get('hubspot_id'),
                'data': result.get('data')
            }), 201
        else:
            return jsonify({'error': result.get('error')}), 400
            
    except ValidationError as e:
        return jsonify({'error': 'Validation error', 'details': e.messages}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ========== EMAIL OPERATIONS ==========

@bp.route('/emails', methods=['GET'])
@jwt_required()
def get_emails():
    """Get all emails from HubSpot"""
    try:
        current_user_id = get_jwt_identity()
        limit = request.args.get('limit', 10, type=int)
        properties = request.args.getlist('properties')
        
        # Get emails from HubSpot
        result = HubSpotService.get_emails(limit=limit, user_id=current_user_id, properties=properties)
        
        # Log the operation
        _create_log(
            user_id=current_user_id,
            session_id=0,
            message_id=0,
            log_type='communication',
            hubspot_id='multiple',
            sync_status='synced'
        )
        
        return jsonify(result), 200
        
    except Exception as e:
        error_msg = str(e)
        # Check if it's a scope issue
        if 'sales-email-read' in error_msg or 'MISSING_SCOPES' in error_msg:
            return jsonify({
                'error': 'Email access requires additional HubSpot permissions',
                'details': 'The HubSpot Personal Access Token needs the "sales-email-read" scope to access emails.',
                'solution': 'Please update your HubSpot app configuration to include the email read scope.',
                'documentation': 'https://developers.hubspot.com/scopes',
                'status_code': 403
            }), 403
        else:
            return jsonify({'error': str(e)}), 500

@bp.route('/emails/<email_id>', methods=['GET'])
@jwt_required()
def get_email(email_id):
    """Get specific email by ID"""
    try:
        current_user_id = get_jwt_identity()
        
        # Get email from HubSpot
        result = HubSpotService.get_email_by_id(email_id)
        
        # Log the operation
        _create_log(
            user_id=current_user_id,
            session_id=0,
            message_id=0,
            log_type='communication',
            hubspot_id=email_id,
            sync_status='synced'
        )
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/emails', methods=['POST'])
@jwt_required()
def create_email():
    """Create email in HubSpot and log to database"""
    try:
        current_user_id = get_jwt_identity()
        data = activity_create_schema.load(request.get_json())
        
        # Create email in HubSpot
        result = HubSpotService.create_email(
            email_data=data['properties'],
            associations=data.get('associations', {}),
            session_id=data['session_id'],
            message_id=data['chat_message_id'],
            user_id=current_user_id
        )
        
        if result.get('success'):
            return jsonify({
                'message': 'Email created successfully',
                'hubspot_id': result.get('hubspot_id'),
                'data': result.get('data')
            }), 201
        else:
            return jsonify({'error': result.get('error')}), 400
            
    except ValidationError as e:
        return jsonify({'error': 'Validation error', 'details': e.messages}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ========== GENERIC ACTIVITY OPERATIONS ==========

@bp.route('/activities', methods=['GET'])
@jwt_required()
def get_activities():
    """Get all activities from HubSpot"""
    try:
        current_user_id = get_jwt_identity()
        activity_type = request.args.get('type', 'all')
        limit = request.args.get('limit', 10, type=int)
        
        # Get activities from HubSpot
        result = HubSpotService.get_activities(
            activity_type=activity_type,
            limit=limit
        )
        
        # Log the operation
        _create_log(
            user_id=current_user_id,
            session_id=0,
            message_id=0,
            log_type='communication',
            hubspot_id='multiple',
            sync_status='synced'
        )
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/activities/search', methods=['POST'])
@jwt_required()
def search_activities():
    """Search activities in HubSpot"""
    try:
        current_user_id = get_jwt_identity()
        data = activity_search_schema.load(request.get_json())
        
        # Search activities in HubSpot
        result = HubSpotService.search_activities(
            activity_type=data['activity_type'],
            search_term=data['search_term'],
            limit=request.args.get('limit', 10, type=int)
        )
        
        # Log the operation
        _create_log(
            user_id=current_user_id,
            session_id=data['session_id'],
            message_id=data['chat_message_id'],
            log_type='communication',
            hubspot_id='search',
            sync_status='synced'
        )
        
        return jsonify(result), 200
        
    except ValidationError as e:
        return jsonify({'error': 'Validation error', 'details': e.messages}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ========== UPDATE OPERATIONS ==========

@bp.route('/activities/<activity_id>', methods=['PATCH'])
@jwt_required()
def update_activity(activity_id):
    """Update activity in HubSpot and log to database"""
    try:
        current_user_id = get_jwt_identity()
        data = activity_update_schema.load(request.get_json())
        
        # Update activity in HubSpot
        result = HubSpotService.update_activity(
            activity_id=activity_id,
            activity_type=data['activity_type'],
            activity_data=data['properties'],
            associations=data.get('associations', {}),
            session_id=data['session_id'],
            message_id=data['chat_message_id'],
            user_id=current_user_id
        )
        
        if result.get('success'):
            return jsonify({
                'message': 'Activity updated successfully',
                'hubspot_id': activity_id,
                'data': result.get('data')
            }), 200
        else:
            return jsonify({'error': result.get('error')}), 400
            
    except ValidationError as e:
        return jsonify({'error': 'Validation error', 'details': e.messages}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ========== DELETE OPERATIONS ==========

@bp.route('/activities/<activity_id>', methods=['DELETE'])
@jwt_required()
def delete_activity(activity_id):
    """Delete activity from HubSpot and log to database"""
    try:
        current_user_id = get_jwt_identity()
        session_id = request.json.get('session_id', 0) if request.is_json else 0
        message_id = request.json.get('chat_message_id', 0) if request.is_json else 0
        
        # Delete activity from HubSpot
        result = HubSpotService.delete_activity(
            activity_id=activity_id,
            session_id=session_id,
            message_id=message_id,
            user_id=current_user_id
        )
        
        if result.get('success'):
            return jsonify({
                'message': 'Activity deleted successfully',
                'hubspot_id': activity_id
            }), 200
        else:
            return jsonify({'error': result.get('error')}), 400
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500
