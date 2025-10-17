"""
HubSpot Deals API - Complete CRUD operations with logging
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.hubspot_service import HubSpotService
from app.models import User, Log, ChatSession, ChatMessage
from app.db.database import db
from marshmallow import Schema, fields, ValidationError
from datetime import datetime

bp = Blueprint('hubspot_deals', __name__)

# Request schemas
class DealCreateSchema(Schema):
    session_id = fields.Int(required=True)
    chat_message_id = fields.Int(required=True)
    properties = fields.Dict(required=True)
    associations = fields.Dict(missing={})

class DealUpdateSchema(Schema):
    session_id = fields.Int(required=True)
    chat_message_id = fields.Int(required=True)
    properties = fields.Dict(required=True)
    associations = fields.Dict(missing={})

class DealSearchSchema(Schema):
    session_id = fields.Int(required=True)
    chat_message_id = fields.Int(required=True)
    search_term = fields.Str(required=True)

# Initialize schemas
deal_create_schema = DealCreateSchema()
deal_update_schema = DealUpdateSchema()
deal_search_schema = DealSearchSchema()

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

@bp.route('/deals', methods=['GET'])
@jwt_required()
def get_deals():
    """Get all deals from HubSpot"""
    try:
        current_user_id = get_jwt_identity()
        limit = request.args.get('limit', 10, type=int)
        properties = request.args.getlist('properties')
        
        # Get deals from HubSpot
        result = HubSpotService.get_deals(limit=limit, user_id=current_user_id, properties=properties)
        
        # Log the operation
        _create_log(
            user_id=current_user_id,
            session_id=0,
            message_id=0,
            log_type='deal',
            hubspot_id='multiple',
            sync_status='synced'
        )
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/deals/<deal_id>', methods=['GET'])
@jwt_required()
def get_deal(deal_id):
    """Get specific deal by ID"""
    try:
        current_user_id = get_jwt_identity()
        
        # Get deal from HubSpot
        result = HubSpotService.get_deal_by_id(deal_id)
        
        # Log the operation
        _create_log(
            user_id=current_user_id,
            session_id=0,
            message_id=0,
            log_type='deal',
            hubspot_id=deal_id,
            sync_status='synced'
        )
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/pipelines', methods=['GET'])
@jwt_required()
def get_deal_pipelines():
    """Get deal pipelines from HubSpot"""
    try:
        current_user_id = get_jwt_identity()
        
        # Get deal pipelines from HubSpot
        result = HubSpotService.get_deal_pipelines(user_id=current_user_id)
        
        # Log the operation
        _create_log(
            user_id=current_user_id,
            session_id=0,
            message_id=0,
            log_type='deal',
            hubspot_id='pipelines',
            sync_status='synced'
        )
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/deals/search', methods=['POST'])
@jwt_required()
def search_deals():
    """Search deals in HubSpot"""
    try:
        current_user_id = get_jwt_identity()
        data = deal_search_schema.load(request.get_json())
        
        # Search deals in HubSpot
        result = HubSpotService.search_deals(
            search_term=data['search_term'],
            limit=request.args.get('limit', 10, type=int)
        )
        
        # Log the operation
        _create_log(
            user_id=current_user_id,
            session_id=data['session_id'],
            message_id=data['chat_message_id'],
            log_type='deal',
            hubspot_id='search',
            sync_status='synced'
        )
        
        return jsonify(result), 200
        
    except ValidationError as e:
        return jsonify({'error': 'Validation error', 'details': e.messages}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ========== CREATE OPERATIONS ==========

@bp.route('/deals', methods=['POST'])
@jwt_required()
def create_deal():
    """Create deal in HubSpot and log to database"""
    try:
        current_user_id = get_jwt_identity()
        data = deal_create_schema.load(request.get_json())
        
        # Create deal in HubSpot
        result = HubSpotService.create_deal(
            deal_data=data['properties'],
            associations=data.get('associations', {}),
            session_id=data['session_id'],
            message_id=data['chat_message_id'],
            user_id=current_user_id
        )
        
        if result.get('success'):
            return jsonify({
                'message': 'Deal created successfully',
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

@bp.route('/deals/<deal_id>', methods=['PATCH'])
@jwt_required()
def update_deal(deal_id):
    """Update deal in HubSpot and log to database"""
    try:
        current_user_id = get_jwt_identity()
        data = deal_update_schema.load(request.get_json())
        
        # Update deal in HubSpot
        result = HubSpotService.update_deal(
            deal_id=deal_id,
            deal_data=data['properties'],
            associations=data.get('associations', {}),
            session_id=data['session_id'],
            message_id=data['chat_message_id'],
            user_id=current_user_id
        )
        
        if result.get('success'):
            return jsonify({
                'message': 'Deal updated successfully',
                'hubspot_id': deal_id,
                'data': result.get('data')
            }), 200
        else:
            return jsonify({'error': result.get('error')}), 400
            
    except ValidationError as e:
        return jsonify({'error': 'Validation error', 'details': e.messages}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/deals/<deal_id>', methods=['PUT'])
@jwt_required()
def replace_deal(deal_id):
    """Replace deal in HubSpot and log to database"""
    try:
        current_user_id = get_jwt_identity()
        data = deal_update_schema.load(request.get_json())
        
        # Replace deal in HubSpot
        result = HubSpotService.replace_deal(
            deal_id=deal_id,
            deal_data=data['properties'],
            associations=data.get('associations', {}),
            session_id=data['session_id'],
            message_id=data['chat_message_id'],
            user_id=current_user_id
        )
        
        if result.get('success'):
            return jsonify({
                'message': 'Deal replaced successfully',
                'hubspot_id': deal_id,
                'data': result.get('data')
            }), 200
        else:
            return jsonify({'error': result.get('error')}), 400
            
    except ValidationError as e:
        return jsonify({'error': 'Validation error', 'details': e.messages}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ========== DELETE OPERATIONS ==========

@bp.route('/deals/<deal_id>', methods=['DELETE'])
@jwt_required()
def delete_deal(deal_id):
    """Delete deal from HubSpot and log to database"""
    try:
        current_user_id = get_jwt_identity()
        session_id = request.json.get('session_id', 0) if request.is_json else 0
        message_id = request.json.get('chat_message_id', 0) if request.is_json else 0
        
        # Delete deal from HubSpot
        result = HubSpotService.delete_deal(
            deal_id=deal_id,
            session_id=session_id,
            message_id=message_id,
            user_id=current_user_id
        )
        
        if result.get('success'):
            return jsonify({
                'message': 'Deal deleted successfully',
                'hubspot_id': deal_id
            }), 200
        else:
            return jsonify({'error': result.get('error')}), 400
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ========== BATCH OPERATIONS ==========

@bp.route('/deals/batch', methods=['POST'])
@jwt_required()
def batch_create_deals():
    """Create multiple deals in batch"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        deals_data = data.get('deals', [])
        session_id = data.get('session_id', 0)
        message_id = data.get('chat_message_id', 0)
        
        # Batch create deals
        result = HubSpotService.batch_create_deals(
            deals_data=deals_data,
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

@bp.route('/deals/batch', methods=['PATCH'])
@jwt_required()
def batch_update_deals():
    """Update multiple deals in batch"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        deals_data = data.get('deals', [])
        session_id = data.get('session_id', 0)
        message_id = data.get('chat_message_id', 0)
        
        # Batch update deals
        result = HubSpotService.batch_update_deals(
            deals_data=deals_data,
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

# ========== PIPELINE OPERATIONS ==========


@bp.route('/deals/pipelines/<pipeline_id>/stages', methods=['GET'])
@jwt_required()
def get_deal_stages(pipeline_id):
    """Get deal stages for a pipeline"""
    try:
        current_user_id = get_jwt_identity()
        
        # Get deal stages from HubSpot
        result = HubSpotService.get_deal_stages(pipeline_id)
        
        # Log the operation
        _create_log(
            user_id=current_user_id,
            session_id=0,
            message_id=0,
            log_type='deal',
            hubspot_id=f'pipeline_{pipeline_id}_stages',
            sync_status='synced'
        )
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
