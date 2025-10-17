"""
HubSpot Notes API - Complete CRUD operations with logging
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.hubspot_service import HubSpotService
from app.models import User, Log, ChatSession, ChatMessage
from app.db.database import db
from marshmallow import Schema, fields, ValidationError
from datetime import datetime

bp = Blueprint('hubspot_notes', __name__)

# Request schemas
class NoteCreateSchema(Schema):
    session_id = fields.Int(required=True)
    chat_message_id = fields.Int(required=True)
    properties = fields.Dict(required=True)
    associations = fields.Dict(missing={})

class NoteUpdateSchema(Schema):
    session_id = fields.Int(required=True)
    chat_message_id = fields.Int(required=True)
    properties = fields.Dict(required=True)
    associations = fields.Dict(missing={})

class NoteSearchSchema(Schema):
    session_id = fields.Int(required=True)
    chat_message_id = fields.Int(required=True)
    search_term = fields.Str(required=True)

# Initialize schemas
note_create_schema = NoteCreateSchema()
note_update_schema = NoteUpdateSchema()
note_search_schema = NoteSearchSchema()

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

@bp.route('/notes', methods=['GET'])
@jwt_required()
def get_notes():
    """Get all notes from HubSpot"""
    try:
        current_user_id = get_jwt_identity()
        limit = request.args.get('limit', 10, type=int)
        properties = request.args.getlist('properties')
        
        # Get notes from HubSpot
        result = HubSpotService.get_notes(limit=limit, user_id=current_user_id, properties=properties)
        
        # Log the operation
        _create_log(
            user_id=current_user_id,
            session_id=0,
            message_id=0,
            log_type='note',
            hubspot_id='multiple',
            sync_status='synced'
        )
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/notes/<note_id>', methods=['GET'])
@jwt_required()
def get_note(note_id):
    """Get specific note by ID"""
    try:
        current_user_id = get_jwt_identity()
        
        # Get note from HubSpot
        result = HubSpotService.get_note_by_id(note_id)
        
        # Log the operation
        _create_log(
            user_id=current_user_id,
            session_id=0,
            message_id=0,
            log_type='note',
            hubspot_id=note_id,
            sync_status='synced'
        )
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/notes/search', methods=['POST'])
@jwt_required()
def search_notes():
    """Search notes in HubSpot"""
    try:
        current_user_id = get_jwt_identity()
        data = note_search_schema.load(request.get_json())
        
        # Search notes in HubSpot
        result = HubSpotService.search_notes(
            search_term=data['search_term'],
            limit=request.args.get('limit', 10, type=int)
        )
        
        # Log the operation
        _create_log(
            user_id=current_user_id,
            session_id=data['session_id'],
            message_id=data['chat_message_id'],
            log_type='note',
            hubspot_id='search',
            sync_status='synced'
        )
        
        return jsonify(result), 200
        
    except ValidationError as e:
        return jsonify({'error': 'Validation error', 'details': e.messages}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ========== CREATE OPERATIONS ==========

@bp.route('/notes', methods=['POST'])
@jwt_required()
def create_note():
    """Create note in HubSpot and log to database"""
    try:
        current_user_id = get_jwt_identity()
        data = note_create_schema.load(request.get_json())
        
        # Create note in HubSpot
        result = HubSpotService.create_note(
            note_data=data['properties'],
            associations=data.get('associations', {}),
            session_id=data['session_id'],
            message_id=data['chat_message_id'],
            user_id=current_user_id
        )
        
        if result.get('success'):
            return jsonify({
                'message': 'Note created successfully',
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

@bp.route('/notes/<note_id>', methods=['PATCH'])
@jwt_required()
def update_note(note_id):
    """Update note in HubSpot and log to database"""
    try:
        current_user_id = get_jwt_identity()
        data = note_update_schema.load(request.get_json())
        
        # Update note in HubSpot
        result = HubSpotService.update_note(
            note_id=note_id,
            note_data=data['properties'],
            associations=data.get('associations', {}),
            session_id=data['session_id'],
            message_id=data['chat_message_id'],
            user_id=current_user_id
        )
        
        if result.get('success'):
            return jsonify({
                'message': 'Note updated successfully',
                'hubspot_id': note_id,
                'data': result.get('data')
            }), 200
        else:
            return jsonify({'error': result.get('error')}), 400
            
    except ValidationError as e:
        return jsonify({'error': 'Validation error', 'details': e.messages}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/notes/<note_id>', methods=['PUT'])
@jwt_required()
def replace_note(note_id):
    """Replace note in HubSpot and log to database"""
    try:
        current_user_id = get_jwt_identity()
        data = note_update_schema.load(request.get_json())
        
        # Replace note in HubSpot
        result = HubSpotService.replace_note(
            note_id=note_id,
            note_data=data['properties'],
            associations=data.get('associations', {}),
            session_id=data['session_id'],
            message_id=data['chat_message_id'],
            user_id=current_user_id
        )
        
        if result.get('success'):
            return jsonify({
                'message': 'Note replaced successfully',
                'hubspot_id': note_id,
                'data': result.get('data')
            }), 200
        else:
            return jsonify({'error': result.get('error')}), 400
            
    except ValidationError as e:
        return jsonify({'error': 'Validation error', 'details': e.messages}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ========== DELETE OPERATIONS ==========

@bp.route('/notes/<note_id>', methods=['DELETE'])
@jwt_required()
def delete_note(note_id):
    """Delete note from HubSpot and log to database"""
    try:
        current_user_id = get_jwt_identity()
        session_id = request.json.get('session_id', 0) if request.is_json else 0
        message_id = request.json.get('chat_message_id', 0) if request.is_json else 0
        
        # Delete note from HubSpot
        result = HubSpotService.delete_note(
            note_id=note_id,
            session_id=session_id,
            message_id=message_id,
            user_id=current_user_id
        )
        
        if result.get('success'):
            return jsonify({
                'message': 'Note deleted successfully',
                'hubspot_id': note_id
            }), 200
        else:
            return jsonify({'error': result.get('error')}), 400
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ========== BATCH OPERATIONS ==========

@bp.route('/notes/batch', methods=['POST'])
@jwt_required()
def batch_create_notes():
    """Create multiple notes in batch"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        notes_data = data.get('notes', [])
        session_id = data.get('session_id', 0)
        message_id = data.get('chat_message_id', 0)
        
        # Batch create notes
        result = HubSpotService.batch_create_notes(
            notes_data=notes_data,
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

@bp.route('/notes/batch', methods=['PATCH'])
@jwt_required()
def batch_update_notes():
    """Update multiple notes in batch"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        notes_data = data.get('notes', [])
        session_id = data.get('session_id', 0)
        message_id = data.get('chat_message_id', 0)
        
        # Batch update notes
        result = HubSpotService.batch_update_notes(
            notes_data=notes_data,
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

# ========== ASSOCIATION OPERATIONS ==========

@bp.route('/notes/<note_id>/associations', methods=['GET'])
@jwt_required()
def get_note_associations(note_id):
    """Get note associations"""
    try:
        current_user_id = get_jwt_identity()
        
        # Get note associations from HubSpot
        result = HubSpotService.get_note_associations(note_id)
        
        # Log the operation
        _create_log(
            user_id=current_user_id,
            session_id=0,
            message_id=0,
            log_type='note',
            hubspot_id=f'{note_id}_associations',
            sync_status='synced'
        )
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/notes/<note_id>/associations', methods=['POST'])
@jwt_required()
def create_note_associations(note_id):
    """Create note associations"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        associations = data.get('associations', {})
        session_id = data.get('session_id', 0)
        message_id = data.get('chat_message_id', 0)
        
        # Create note associations in HubSpot
        result = HubSpotService.create_note_associations(
            note_id=note_id,
            associations=associations,
            session_id=session_id,
            message_id=message_id,
            user_id=current_user_id
        )
        
        if result.get('success'):
            return jsonify({
                'message': 'Note associations created successfully',
                'hubspot_id': note_id
            }), 200
        else:
            return jsonify({'error': result.get('error')}), 400
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500
