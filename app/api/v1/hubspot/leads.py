"""
HubSpot Leads API - Lead management and qualification
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.hubspot_service import HubSpotService
from app.models import User, Log, ChatSession, ChatMessage
from app.db.database import db
from marshmallow import Schema, fields, ValidationError
from datetime import datetime

bp = Blueprint('hubspot_leads', __name__)

# Request schemas
class LeadCreateSchema(Schema):
    session_id = fields.Int(required=True)
    chat_message_id = fields.Int(required=True)
    firstname = fields.Str(required=True)
    lastname = fields.Str(required=True)
    email = fields.Str(required=True)
    phone = fields.Str(missing='')
    company = fields.Str(missing='')
    lead_source = fields.Str(missing='WhatsApp')
    lead_status = fields.Str(missing='NEW')

class LeadQualifySchema(Schema):
    session_id = fields.Int(required=True)
    chat_message_id = fields.Int(required=True)
    lead_status = fields.Str(missing='QUALIFIED')
    create_deal = fields.Bool(missing=False)
    deal_name = fields.Str(missing='')
    deal_amount = fields.Str(missing='')
    deal_stage = fields.Str(missing='appointmentscheduled')
    close_date = fields.Str(missing='')

class DealStageUpdateSchema(Schema):
    session_id = fields.Int(required=True)
    chat_message_id = fields.Int(required=True)
    new_stage = fields.Str(required=True)
    reason = fields.Str(missing='')

# Initialize schemas
lead_create_schema = LeadCreateSchema()
lead_qualify_schema = LeadQualifySchema()
deal_stage_update_schema = DealStageUpdateSchema()

def _create_log(user_id, session_id, message_id, log_type, hubspot_id, sync_status, sync_error=None, 
                lead_status=None, deal_stage=None, lead_source=None, deal_amount=None, stage_reason=None):
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
            synced_at=datetime.utcnow() if sync_status == 'synced' else None,
            lead_status=lead_status,
            deal_stage=deal_stage,
            lead_source=lead_source,
            deal_amount=deal_amount,
            stage_reason=stage_reason
        )
        db.session.add(log)
        db.session.commit()
        return log
    except Exception as e:
        db.session.rollback()
        return None

# ========== LEAD OPERATIONS ==========

@bp.route('/leads', methods=['GET'])
@jwt_required()
def get_leads():
    """Get all leads from HubSpot"""
    try:
        current_user_id = get_jwt_identity()
        limit = request.args.get('limit', 10, type=int)
        lead_status = request.args.get('lead_status', '')
        
        # Get leads from HubSpot
        filters = {}
        if lead_status:
            filters['lead_status'] = lead_status
            
        result = HubSpotService.get_leads(limit=limit, user_id=current_user_id, **filters)
        
        # Log the operation
        _create_log(
            user_id=current_user_id,
            session_id=0,
            message_id=0,
            log_type='contact_action',
            hubspot_id='leads',
            sync_status='synced'
        )
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/leads', methods=['POST'])
@jwt_required()
def create_lead():
    """Create a new lead in HubSpot"""
    try:
        current_user_id = get_jwt_identity()
        data = lead_create_schema.load(request.get_json())
        
        # Create lead in HubSpot
        result = HubSpotService.create_lead(
            lead_data=data,
            session_id=data['session_id'],
            message_id=data['chat_message_id'],
            user_id=current_user_id
        )
        
        if result['success']:
            # Log the lead creation with detailed information
            _create_log(
                user_id=current_user_id,
                session_id=data['session_id'],
                message_id=data['chat_message_id'],
                log_type='lead',
                hubspot_id=result['hubspot_id'],
                sync_status='synced',
                lead_status=data.get('lead_status', 'NEW'),
                lead_source=data.get('lead_source', 'WhatsApp')
            )
            
            return jsonify({
                'success': True,
                'hubspot_id': result['hubspot_id'],
                'data': result['data'],
                'message': 'Lead created successfully'
            }), 201
        else:
            return jsonify({
                'success': False,
                'error': result['error']
            }), 400
            
    except ValidationError as e:
        return jsonify({'error': 'Validation error', 'details': e.messages}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/leads/<lead_id>/qualify', methods=['POST'])
@jwt_required()
def qualify_lead(lead_id):
    """Qualify a lead and optionally create a deal"""
    try:
        current_user_id = get_jwt_identity()
        data = lead_qualify_schema.load(request.get_json())
        
        # Qualify lead in HubSpot
        result = HubSpotService.qualify_lead(
            contact_id=lead_id,
            qualification_data=data,
            user_id=current_user_id
        )
        
        if result['success']:
            # Log the qualification
            _create_log(
                user_id=current_user_id,
                session_id=data['session_id'],
                message_id=data['chat_message_id'],
                log_type='lead_qualification',
                hubspot_id=lead_id,
                sync_status='synced',
                lead_status=data.get('lead_status', 'QUALIFIED')
            )
            
            # Log deal creation if applicable
            if result.get('deal_created') and result.get('deal_id'):
                _create_log(
                    user_id=current_user_id,
                    session_id=data['session_id'],
                    message_id=data['chat_message_id'],
                    log_type='deal',
                    hubspot_id=result['deal_id'],
                    sync_status='synced',
                    deal_stage=data.get('deal_stage', 'appointmentscheduled'),
                    deal_amount=data.get('deal_amount', '')
                )
            
            return jsonify({
                'success': True,
                'contact_updated': result['contact_updated'],
                'deal_created': result['deal_created'],
                'deal_id': result.get('deal_id'),
                'message': 'Lead qualified successfully'
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to qualify lead'
            }), 400
            
    except ValidationError as e:
        return jsonify({'error': 'Validation error', 'details': e.messages}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ========== DEAL STAGE OPERATIONS ==========

@bp.route('/deals/<deal_id>/stages', methods=['PATCH'])
@jwt_required()
def update_deal_stage(deal_id):
    """Update deal stage"""
    try:
        current_user_id = get_jwt_identity()
        data = deal_stage_update_schema.load(request.get_json())
        
        # Update deal stage in HubSpot
        result = HubSpotService.update_deal_stage(
            deal_id=deal_id,
            new_stage=data['new_stage'],
            user_id=current_user_id
        )
        
        # Log the operation
        _create_log(
            user_id=current_user_id,
            session_id=data['session_id'],
            message_id=data['chat_message_id'],
            log_type='deal_stage_update',
            hubspot_id=deal_id,
            sync_status='synced',
            deal_stage=data['new_stage'],
            stage_reason=data.get('reason', '')
        )
        
        return jsonify({
            'success': True,
            'deal_id': deal_id,
            'new_stage': data['new_stage'],
            'data': result,
            'message': 'Deal stage updated successfully'
        }), 200
        
    except ValidationError as e:
        return jsonify({'error': 'Validation error', 'details': e.messages}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/pipelines/<pipeline_id>/stages', methods=['GET'])
@jwt_required()
def get_deal_stages(pipeline_id):
    """Get deal stages for a pipeline"""
    try:
        current_user_id = get_jwt_identity()
        
        # Get deal stages from HubSpot
        result = HubSpotService.get_deal_stages(pipeline_id, user_id=current_user_id)
        
        # Log the operation
        _create_log(
            user_id=current_user_id,
            session_id=0,
            message_id=0,
            log_type='deal',
            hubspot_id=f'pipeline_{pipeline_id}',
            sync_status='synced'
        )
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/pipelines', methods=['GET'])
@jwt_required()
def get_deal_pipelines():
    """Get all deal pipelines"""
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

# ========== LEAD ANALYTICS ==========

@bp.route('/leads/analytics', methods=['GET'])
@jwt_required()
def get_lead_analytics():
    """Get lead analytics and statistics"""
    try:
        current_user_id = get_jwt_identity()
        
        # Get leads for analytics
        leads_result = HubSpotService.get_leads(limit=100, user_id=current_user_id)
        leads = leads_result.get('results', [])
        
        # Calculate analytics
        total_leads = len(leads)
        lead_statuses = {}
        lead_sources = {}
        
        for lead in leads:
            properties = lead.get('properties', {})
            status = properties.get('lead_status', 'UNKNOWN')
            source = properties.get('lead_source', 'UNKNOWN')
            
            lead_statuses[status] = lead_statuses.get(status, 0) + 1
            lead_sources[source] = lead_sources.get(source, 0) + 1
        
        analytics = {
            'total_leads': total_leads,
            'lead_statuses': lead_statuses,
            'lead_sources': lead_sources,
            'conversion_rate': 0  # This would need more complex calculation
        }
        
        return jsonify(analytics), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
