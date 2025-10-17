"""
HubSpot Associations API - Link objects together with logging
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.hubspot_service import HubSpotService
from app.models import User, Log, ChatSession, ChatMessage
from app.db.database import db
from marshmallow import Schema, fields, ValidationError
from datetime import datetime

bp = Blueprint('hubspot_associations', __name__)

# Request schemas
class AssociationCreateSchema(Schema):
    session_id = fields.Int(required=True)
    chat_message_id = fields.Int(required=True)
    from_object_type = fields.Str(required=True)
    from_object_id = fields.Str(required=True)
    to_object_type = fields.Str(required=True)
    to_object_id = fields.Str(required=True)
    association_type = fields.Str(missing='default')

class AssociationBatchSchema(Schema):
    session_id = fields.Int(required=True)
    chat_message_id = fields.Int(required=True)
    associations = fields.List(fields.Dict(), required=True)

class AssociationSearchSchema(Schema):
    session_id = fields.Int(required=True)
    chat_message_id = fields.Int(required=True)
    object_type = fields.Str(required=True)
    object_id = fields.Str(required=True)

# Initialize schemas
association_create_schema = AssociationCreateSchema()
association_batch_schema = AssociationBatchSchema()
association_search_schema = AssociationSearchSchema()

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

# ========== GET ASSOCIATION TYPES ==========

@bp.route('/types', methods=['GET'])
@jwt_required()
def get_association_types():
    """Get association types from HubSpot"""
    try:
        current_user_id = get_jwt_identity()
        
        # Get association types from HubSpot
        result = HubSpotService.get_association_types(user_id=current_user_id)
        
        # Log the operation
        _create_log(
            user_id=current_user_id,
            session_id=0,
            message_id=0,
            log_type='association',
            hubspot_id='types',
            sync_status='synced'
        )
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ========== CREATE ASSOCIATIONS ==========

@bp.route('/associations', methods=['POST'])
@jwt_required()
def create_association():
    """Create association between two objects"""
    try:
        current_user_id = get_jwt_identity()
        data = association_create_schema.load(request.get_json())
        
        # Create association in HubSpot
        result = HubSpotService.create_association(
            from_object_type=data['from_object_type'],
            from_object_id=data['from_object_id'],
            to_object_type=data['to_object_type'],
            to_object_id=data['to_object_id'],
            association_type=data['association_type'],
            session_id=data['session_id'],
            message_id=data['chat_message_id'],
            user_id=current_user_id
        )
        
        if result.get('success'):
            return jsonify({
                'message': 'Association created successfully',
                'from_object': f"{data['from_object_type']}:{data['from_object_id']}",
                'to_object': f"{data['to_object_type']}:{data['to_object_id']}"
            }), 201
        else:
            return jsonify({'error': result.get('error')}), 400
            
    except ValidationError as e:
        return jsonify({'error': 'Validation error', 'details': e.messages}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/associations/batch', methods=['POST'])
@jwt_required()
def batch_create_associations():
    """Create multiple associations in batch"""
    try:
        current_user_id = get_jwt_identity()
        data = association_batch_schema.load(request.get_json())
        
        # Batch create associations
        result = HubSpotService.batch_create_associations(
            associations=data['associations'],
            session_id=data['session_id'],
            message_id=data['chat_message_id'],
            user_id=current_user_id
        )
        
        return jsonify({
            'message': f'Batch association operation completed',
            'results': result
        }), 200
        
    except ValidationError as e:
        return jsonify({'error': 'Validation error', 'details': e.messages}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ========== GET ASSOCIATIONS ==========

@bp.route('/associations/<object_type>/<object_id>', methods=['GET'])
@jwt_required()
def get_object_associations(object_type, object_id):
    """Get all associations for a specific object"""
    try:
        current_user_id = get_jwt_identity()
        to_object_type = request.args.get('to_object_type')
        limit = request.args.get('limit', 10, type=int)
        
        # Get associations from HubSpot
        result = HubSpotService.get_object_associations(
            object_type=object_type,
            object_id=object_id,
            to_object_type=to_object_type,
            limit=limit
        )
        
        # Log the operation
        _create_log(
            user_id=current_user_id,
            session_id=0,
            message_id=0,
            log_type='association',
            hubspot_id=f'{object_type}_{object_id}',
            sync_status='synced'
        )
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/associations/search', methods=['POST'])
@jwt_required()
def search_associations():
    """Search associations for a specific object"""
    try:
        current_user_id = get_jwt_identity()
        data = association_search_schema.load(request.get_json())
        
        # Search associations in HubSpot
        result = HubSpotService.search_associations(
            object_type=data['object_type'],
            object_id=data['object_id'],
            limit=request.args.get('limit', 10, type=int)
        )
        
        # Log the operation
        _create_log(
            user_id=current_user_id,
            session_id=data['session_id'],
            message_id=data['chat_message_id'],
            log_type='association',
            hubspot_id=f'{data["object_type"]}_{data["object_id"]}',
            sync_status='synced'
        )
        
        return jsonify(result), 200
        
    except ValidationError as e:
        return jsonify({'error': 'Validation error', 'details': e.messages}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ========== DELETE ASSOCIATIONS ==========

@bp.route('/associations/<object_type>/<object_id>/<to_object_type>/<to_object_id>', methods=['DELETE'])
@jwt_required()
def delete_association(object_type, object_id, to_object_type, to_object_id):
    """Delete association between two objects"""
    try:
        current_user_id = get_jwt_identity()
        session_id = request.json.get('session_id', 0) if request.is_json else 0
        message_id = request.json.get('chat_message_id', 0) if request.is_json else 0
        
        # Delete association from HubSpot
        result = HubSpotService.delete_association(
            from_object_type=object_type,
            from_object_id=object_id,
            to_object_type=to_object_type,
            to_object_id=to_object_id,
            session_id=session_id,
            message_id=message_id,
            user_id=current_user_id
        )
        
        if result.get('success'):
            return jsonify({
                'message': 'Association deleted successfully',
                'from_object': f"{object_type}:{object_id}",
                'to_object': f"{to_object_type}:{to_object_id}"
            }), 200
        else:
            return jsonify({'error': result.get('error')}), 400
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ========== SPECIFIC ASSOCIATION TYPES ==========

@bp.route('/associations/contact-deal', methods=['POST'])
@jwt_required()
def associate_contact_deal():
    """Associate contact with deal"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        contact_id = data.get('contact_id')
        deal_id = data.get('deal_id')
        session_id = data.get('session_id', 0)
        message_id = data.get('chat_message_id', 0)
        
        # Create contact-deal association
        result = HubSpotService.create_association(
            from_object_type='contacts',
            from_object_id=contact_id,
            to_object_type='deals',
            to_object_id=deal_id,
            association_type='contact_to_deal',
            session_id=session_id,
            message_id=message_id,
            user_id=current_user_id
        )
        
        if result.get('success'):
            return jsonify({
                'message': 'Contact-Deal association created successfully',
                'contact_id': contact_id,
                'deal_id': deal_id
            }), 201
        else:
            return jsonify({'error': result.get('error')}), 400
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/associations/contact-company', methods=['POST'])
@jwt_required()
def associate_contact_company():
    """Associate contact with company"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        contact_id = data.get('contact_id')
        company_id = data.get('company_id')
        session_id = data.get('session_id', 0)
        message_id = data.get('chat_message_id', 0)
        
        # Create contact-company association
        result = HubSpotService.create_association(
            from_object_type='contacts',
            from_object_id=contact_id,
            to_object_type='companies',
            to_object_id=company_id,
            association_type='contact_to_company',
            session_id=session_id,
            message_id=message_id,
            user_id=current_user_id
        )
        
        if result.get('success'):
            return jsonify({
                'message': 'Contact-Company association created successfully',
                'contact_id': contact_id,
                'company_id': company_id
            }), 201
        else:
            return jsonify({'error': result.get('error')}), 400
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/associations/deal-company', methods=['POST'])
@jwt_required()
def associate_deal_company():
    """Associate deal with company"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        deal_id = data.get('deal_id')
        company_id = data.get('company_id')
        session_id = data.get('session_id', 0)
        message_id = data.get('chat_message_id', 0)
        
        # Create deal-company association
        result = HubSpotService.create_association(
            from_object_type='deals',
            from_object_id=deal_id,
            to_object_type='companies',
            to_object_id=company_id,
            association_type='deal_to_company',
            session_id=session_id,
            message_id=message_id,
            user_id=current_user_id
        )
        
        if result.get('success'):
            return jsonify({
                'message': 'Deal-Company association created successfully',
                'deal_id': deal_id,
                'company_id': company_id
            }), 201
        else:
            return jsonify({'error': result.get('error')}), 400
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ========== ASSOCIATION TYPES ==========


@bp.route('/associations/types/<object_type>', methods=['GET'])
@jwt_required()
def get_object_association_types(object_type):
    """Get association types for specific object type"""
    try:
        current_user_id = get_jwt_identity()
        
        # Get object association types from HubSpot
        result = HubSpotService.get_object_association_types(object_type)
        
        # Log the operation
        _create_log(
            user_id=current_user_id,
            session_id=0,
            message_id=0,
            log_type='association',
            hubspot_id=f'{object_type}_types',
            sync_status='synced'
        )
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
