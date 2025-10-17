"""
HubSpot Companies API - Complete CRUD operations with logging
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.hubspot_service import HubSpotService
from app.models import User, Log, ChatSession, ChatMessage
from app.db.database import db
from marshmallow import Schema, fields, ValidationError
from datetime import datetime

bp = Blueprint('hubspot_companies', __name__)

# Request schemas
class CompanyCreateSchema(Schema):
    session_id = fields.Int(required=True)
    chat_message_id = fields.Int(required=True)
    properties = fields.Dict(required=True)

class CompanyUpdateSchema(Schema):
    session_id = fields.Int(required=True)
    chat_message_id = fields.Int(required=True)
    properties = fields.Dict(required=True)

class CompanySearchSchema(Schema):
    session_id = fields.Int(required=True)
    chat_message_id = fields.Int(required=True)
    search_term = fields.Str(required=True)

# Initialize schemas
company_create_schema = CompanyCreateSchema()
company_update_schema = CompanyUpdateSchema()
company_search_schema = CompanySearchSchema()

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
@jwt_required()
def get_companies():
    """Get all companies from HubSpot"""
    try:
        current_user_id = get_jwt_identity()
        limit = request.args.get('limit', 10, type=int)
        properties = request.args.getlist('properties')
        
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
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/companies/<company_id>', methods=['GET'])
@jwt_required()
def get_company(company_id):
    """Get specific company by ID"""
    try:
        current_user_id = get_jwt_identity()
        
        # Get company from HubSpot
        result = HubSpotService.get_company_by_id(company_id)
        
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
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/properties', methods=['GET'])
@jwt_required()
def get_company_properties():
    """Get company properties from HubSpot"""
    try:
        current_user_id = get_jwt_identity()
        
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
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/companies/search', methods=['POST'])
@jwt_required()
def search_companies():
    """Search companies in HubSpot"""
    try:
        current_user_id = get_jwt_identity()
        data = company_search_schema.load(request.get_json())
        
        # Search companies in HubSpot
        result = HubSpotService.search_companies(
            search_term=data['search_term'],
            limit=request.args.get('limit', 10, type=int)
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
@jwt_required()
def create_company():
    """Create company in HubSpot and log to database"""
    try:
        current_user_id = get_jwt_identity()
        data = company_create_schema.load(request.get_json())
        
        # Create company in HubSpot
        result = HubSpotService.create_company(
            company_data=data['properties'],
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

@bp.route('/companies/<company_id>', methods=['PATCH'])
@jwt_required()
def update_company(company_id):
    """Update company in HubSpot and log to database"""
    try:
        current_user_id = get_jwt_identity()
        data = company_update_schema.load(request.get_json())
        
        # Update company in HubSpot
        result = HubSpotService.update_company(
            company_id=company_id,
            company_data=data['properties'],
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

@bp.route('/companies/<company_id>', methods=['PUT'])
@jwt_required()
def replace_company(company_id):
    """Replace company in HubSpot and log to database"""
    try:
        current_user_id = get_jwt_identity()
        data = company_update_schema.load(request.get_json())
        
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

@bp.route('/companies/<company_id>', methods=['DELETE'])
@jwt_required()
def delete_company(company_id):
    """Delete company from HubSpot and log to database"""
    try:
        current_user_id = get_jwt_identity()
        session_id = request.json.get('session_id', 0) if request.is_json else 0
        message_id = request.json.get('chat_message_id', 0) if request.is_json else 0
        
        # Delete company from HubSpot
        result = HubSpotService.delete_company(
            company_id=company_id,
            session_id=session_id,
            message_id=message_id,
            user_id=current_user_id
        )
        
        if result.get('success'):
            return jsonify({
                'message': 'Company deleted successfully',
                'hubspot_id': company_id
            }), 200
        else:
            return jsonify({'error': result.get('error')}), 400
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ========== BATCH OPERATIONS ==========

@bp.route('/companies/batch', methods=['POST'])
@jwt_required()
def batch_create_companies():
    """Create multiple companies in batch"""
    try:
        current_user_id = get_jwt_identity()
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
@jwt_required()
def batch_update_companies():
    """Update multiple companies in batch"""
    try:
        current_user_id = get_jwt_identity()
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


@bp.route('/companies/properties/<property_name>', methods=['GET'])
@jwt_required()
def get_company_property(property_name):
    """Get specific company property schema"""
    try:
        current_user_id = get_jwt_identity()
        
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
