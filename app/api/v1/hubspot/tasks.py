"""
HubSpot Tasks API - Complete CRUD operations with logging
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.hubspot_service import HubSpotService
from app.models import User, Log, ChatSession, ChatMessage
from app.db.database import db
from marshmallow import Schema, fields, ValidationError
from datetime import datetime

bp = Blueprint('hubspot_tasks', __name__)

# Request schemas
class TaskCreateSchema(Schema):
    session_id = fields.Int(required=True)
    chat_message_id = fields.Int(required=True)
    properties = fields.Dict(required=True)
    associations = fields.Dict(missing={})

class TaskUpdateSchema(Schema):
    session_id = fields.Int(required=True)
    chat_message_id = fields.Int(required=True)
    properties = fields.Dict(required=True)
    associations = fields.Dict(missing={})

class TaskSearchSchema(Schema):
    session_id = fields.Int(required=True)
    chat_message_id = fields.Int(required=True)
    search_term = fields.Str(required=True)

# Initialize schemas
task_create_schema = TaskCreateSchema()
task_update_schema = TaskUpdateSchema()
task_search_schema = TaskSearchSchema()

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

@bp.route('/tasks', methods=['GET'])
@jwt_required()
def get_tasks():
    """Get all tasks from HubSpot"""
    try:
        current_user_id = get_jwt_identity()
        limit = request.args.get('limit', 10, type=int)
        properties = request.args.getlist('properties')
        
        # Get tasks from HubSpot
        result = HubSpotService.get_tasks(limit=limit, user_id=current_user_id, properties=properties)
        
        # Log the operation
        _create_log(
            user_id=current_user_id,
            session_id=0,
            message_id=0,
            log_type='task',
            hubspot_id='multiple',
            sync_status='synced'
        )
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/tasks/<task_id>', methods=['GET'])
@jwt_required()
def get_task(task_id):
    """Get specific task by ID"""
    try:
        current_user_id = get_jwt_identity()
        
        # Get task from HubSpot
        result = HubSpotService.get_task_by_id(task_id)
        
        # Log the operation
        _create_log(
            user_id=current_user_id,
            session_id=0,
            message_id=0,
            log_type='task',
            hubspot_id=task_id,
            sync_status='synced'
        )
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/tasks/search', methods=['POST'])
@jwt_required()
def search_tasks():
    """Search tasks in HubSpot"""
    try:
        current_user_id = get_jwt_identity()
        data = task_search_schema.load(request.get_json())
        
        # Search tasks in HubSpot
        result = HubSpotService.search_tasks(
            search_term=data['search_term'],
            limit=request.args.get('limit', 10, type=int)
        )
        
        # Log the operation
        _create_log(
            user_id=current_user_id,
            session_id=data['session_id'],
            message_id=data['chat_message_id'],
            log_type='task',
            hubspot_id='search',
            sync_status='synced'
        )
        
        return jsonify(result), 200
        
    except ValidationError as e:
        return jsonify({'error': 'Validation error', 'details': e.messages}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ========== CREATE OPERATIONS ==========

@bp.route('/tasks', methods=['POST'])
@jwt_required()
def create_task():
    """Create task in HubSpot and log to database"""
    try:
        current_user_id = get_jwt_identity()
        data = task_create_schema.load(request.get_json())
        
        # Create task in HubSpot
        result = HubSpotService.create_task(
            task_data=data['properties'],
            associations=data.get('associations', {}),
            session_id=data['session_id'],
            message_id=data['chat_message_id'],
            user_id=current_user_id
        )
        
        if result.get('success'):
            return jsonify({
                'message': 'Task created successfully',
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

@bp.route('/tasks/<task_id>', methods=['PATCH'])
@jwt_required()
def update_task(task_id):
    """Update task in HubSpot and log to database"""
    try:
        current_user_id = get_jwt_identity()
        data = task_update_schema.load(request.get_json())
        
        # Update task in HubSpot
        result = HubSpotService.update_task(
            task_id=task_id,
            task_data=data['properties'],
            associations=data.get('associations', {}),
            session_id=data['session_id'],
            message_id=data['chat_message_id'],
            user_id=current_user_id
        )
        
        if result.get('success'):
            return jsonify({
                'message': 'Task updated successfully',
                'hubspot_id': task_id,
                'data': result.get('data')
            }), 200
        else:
            return jsonify({'error': result.get('error')}), 400
            
    except ValidationError as e:
        return jsonify({'error': 'Validation error', 'details': e.messages}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/tasks/<task_id>', methods=['PUT'])
@jwt_required()
def replace_task(task_id):
    """Replace task in HubSpot and log to database"""
    try:
        current_user_id = get_jwt_identity()
        data = task_update_schema.load(request.get_json())
        
        # Replace task in HubSpot
        result = HubSpotService.replace_task(
            task_id=task_id,
            task_data=data['properties'],
            associations=data.get('associations', {}),
            session_id=data['session_id'],
            message_id=data['chat_message_id'],
            user_id=current_user_id
        )
        
        if result.get('success'):
            return jsonify({
                'message': 'Task replaced successfully',
                'hubspot_id': task_id,
                'data': result.get('data')
            }), 200
        else:
            return jsonify({'error': result.get('error')}), 400
            
    except ValidationError as e:
        return jsonify({'error': 'Validation error', 'details': e.messages}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ========== DELETE OPERATIONS ==========

@bp.route('/tasks/<task_id>', methods=['DELETE'])
@jwt_required()
def delete_task(task_id):
    """Delete task from HubSpot and log to database"""
    try:
        current_user_id = get_jwt_identity()
        session_id = request.json.get('session_id', 0) if request.is_json else 0
        message_id = request.json.get('chat_message_id', 0) if request.is_json else 0
        
        # Delete task from HubSpot
        result = HubSpotService.delete_task(
            task_id=task_id,
            session_id=session_id,
            message_id=message_id,
            user_id=current_user_id
        )
        
        if result.get('success'):
            return jsonify({
                'message': 'Task deleted successfully',
                'hubspot_id': task_id
            }), 200
        else:
            return jsonify({'error': result.get('error')}), 400
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ========== BATCH OPERATIONS ==========

@bp.route('/tasks/batch', methods=['POST'])
@jwt_required()
def batch_create_tasks():
    """Create multiple tasks in batch"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        tasks_data = data.get('tasks', [])
        session_id = data.get('session_id', 0)
        message_id = data.get('chat_message_id', 0)
        
        # Batch create tasks
        result = HubSpotService.batch_create_tasks(
            tasks_data=tasks_data,
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

@bp.route('/tasks/batch', methods=['PATCH'])
@jwt_required()
def batch_update_tasks():
    """Update multiple tasks in batch"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        tasks_data = data.get('tasks', [])
        session_id = data.get('session_id', 0)
        message_id = data.get('chat_message_id', 0)
        
        # Batch update tasks
        result = HubSpotService.batch_update_tasks(
            tasks_data=tasks_data,
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

# ========== STATUS OPERATIONS ==========

@bp.route('/tasks/<task_id>/complete', methods=['POST'])
@jwt_required()
def complete_task(task_id):
    """Mark task as completed"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        session_id = data.get('session_id', 0)
        message_id = data.get('chat_message_id', 0)
        
        # Complete task in HubSpot
        result = HubSpotService.complete_task(
            task_id=task_id,
            session_id=session_id,
            message_id=message_id,
            user_id=current_user_id
        )
        
        if result.get('success'):
            return jsonify({
                'message': 'Task completed successfully',
                'hubspot_id': task_id
            }), 200
        else:
            return jsonify({'error': result.get('error')}), 400
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/tasks/<task_id>/status', methods=['PATCH'])
@jwt_required()
def update_task_status(task_id):
    """Update task status"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        status = data.get('status')
        session_id = data.get('session_id', 0)
        message_id = data.get('chat_message_id', 0)
        
        # Update task status in HubSpot
        result = HubSpotService.update_task_status(
            task_id=task_id,
            status=status,
            session_id=session_id,
            message_id=message_id,
            user_id=current_user_id
        )
        
        if result.get('success'):
            return jsonify({
                'message': 'Task status updated successfully',
                'hubspot_id': task_id
            }), 200
        else:
            return jsonify({'error': result.get('error')}), 400
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500
