"""
WhatsApp Webhook Controller for Twilio Integration
Handles incoming WhatsApp messages and processes them with AI
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import User, ChatSession, ChatMessage, Log
from app.db.database import db
from datetime import datetime
import json
import logging

bp = Blueprint('whatsapp', __name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def _create_log(user_id, session_id, message_id, log_type, hubspot_id, sync_status, sync_error=None):
    """Create a log entry for WhatsApp operations"""
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
        logger.error(f"Failed to create log: {e}")
        return None

@bp.route('/webhook', methods=['GET', 'POST'])
def webhook():
    """
    Twilio WhatsApp Webhook Endpoint
    GET: Verify webhook (Twilio verification)
    POST: Handle incoming messages
    """
    if request.method == 'GET':
        # Twilio webhook verification
        return request.args.get('hub.challenge', ''), 200
    
    elif request.method == 'POST':
        try:
            # Parse Twilio webhook data
            data = request.get_json()
            logger.info(f"Received WhatsApp webhook: {json.dumps(data, indent=2)}")
            
            # Extract message details
            message_data = data.get('entry', [{}])[0].get('changes', [{}])[0].get('value', {})
            messages = message_data.get('messages', [])
            
            if not messages:
                logger.warning("No messages found in webhook data")
                return jsonify({'status': 'no_messages'}), 200
            
            # Process each message
            for message in messages:
                process_whatsapp_message(message, message_data)
            
            return jsonify({'status': 'success'}), 200
            
        except Exception as e:
            logger.error(f"Error processing WhatsApp webhook: {e}")
            return jsonify({'error': str(e)}), 500

def process_whatsapp_message(message, message_data):
    """Process individual WhatsApp message"""
    try:
        # Extract message details
        message_id = message.get('id')
        from_number = message.get('from')
        message_text = message.get('text', {}).get('body', '')
        timestamp = message.get('timestamp')
        
        logger.info(f"Processing message {message_id} from {from_number}: {message_text}")
        
        # Find or create user by phone number
        user = User.query.filter_by(phone_number=from_number).first()
        if not user:
            logger.warning(f"No user found for phone number: {from_number}")
            return
        
        # Find or create chat session
        session = ChatSession.query.filter_by(
            user_id=user.id,
            status='active'
        ).first()
        
        if not session:
            session = ChatSession(
                user_id=user.id,
                started_at=datetime.utcnow(),
                status='active'
            )
            db.session.add(session)
            db.session.commit()
            logger.info(f"Created new chat session {session.id} for user {user.id}")
        
        # Create chat message record
        chat_message = ChatMessage(
            session_id=session.id,
            message_text=message_text,
            timestamp=datetime.fromtimestamp(int(timestamp)),
            forwarded_from=from_number
        )
        db.session.add(chat_message)
        db.session.commit()
        
        logger.info(f"Created chat message {chat_message.id} in session {session.id}")
        
        # Log the incoming message
        _create_log(
            user_id=user.id,
            session_id=session.id,
            message_id=chat_message.id,
            log_type='whatsapp_message',
            hubspot_id=message_id,
            sync_status='synced'
        )
        
        # Here you would typically:
        # 1. Send message to AI for analysis
        # 2. AI determines what HubSpot actions to take
        # 3. Execute HubSpot API calls based on AI analysis
        # 4. Send response back to user via Twilio
        
        logger.info(f"Message {message_id} processed successfully")
        
    except Exception as e:
        logger.error(f"Error processing message {message_id}: {e}")

@bp.route('/send', methods=['POST'])
@jwt_required()
def send_message():
    """
    Send WhatsApp message via Twilio
    This endpoint can be called by your n8n workflow
    """
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        to_number = data.get('to')
        message_text = data.get('message')
        session_id = data.get('session_id')
        message_id = data.get('message_id')
        
        if not all([to_number, message_text]):
            return jsonify({'error': 'Missing required fields: to, message'}), 400
        
        # Here you would integrate with Twilio API to send the message
        # For now, we'll just log it
        logger.info(f"Sending WhatsApp message to {to_number}: {message_text}")
        
        # Log the outgoing message
        _create_log(
            user_id=current_user_id,
            session_id=session_id or 0,
            message_id=message_id or 0,
            log_type='whatsapp_send',
            hubspot_id='outgoing',
            sync_status='synced'
        )
        
        return jsonify({
            'status': 'success',
            'message': 'WhatsApp message queued for sending',
            'to': to_number,
            'text': message_text
        }), 200
        
    except Exception as e:
        logger.error(f"Error sending WhatsApp message: {e}")
        return jsonify({'error': str(e)}), 500

@bp.route('/status', methods=['GET'])
def status():
    """WhatsApp integration status"""
    try:
        # Count active sessions
        active_sessions = ChatSession.query.filter_by(status='active').count()
        
        # Count recent messages
        recent_messages = ChatMessage.query.filter(
            ChatMessage.timestamp >= datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        ).count()
        
        return jsonify({
            'status': 'active',
            'active_sessions': active_sessions,
            'recent_messages': recent_messages,
            'webhook_url': '/api/whatsapp/webhook',
            'timestamp': datetime.utcnow().isoformat()
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting WhatsApp status: {e}")
        return jsonify({'error': str(e)}), 500

@bp.route('/sessions', methods=['GET'])
@jwt_required()
def get_sessions():
    """Get all chat sessions for the current user"""
    try:
        current_user_id = get_jwt_identity()
        
        sessions = ChatSession.query.filter_by(user_id=current_user_id).order_by(
            ChatSession.created_at.desc()
        ).all()
        
        sessions_data = []
        for session in sessions:
            messages = ChatMessage.query.filter_by(session_id=session.id).order_by(
                ChatMessage.timestamp
            ).all()
            
            sessions_data.append({
                'id': session.id,
                'started_at': session.started_at.isoformat(),
                'ended_at': session.ended_at.isoformat() if session.ended_at else None,
                'status': session.status,
                'message_count': len(messages),
                'messages': [{
                    'id': msg.id,
                    'text': msg.message_text,
                    'timestamp': msg.timestamp.isoformat(),
                    'from': msg.forwarded_from
                } for msg in messages]
            })
        
        return jsonify({
            'sessions': sessions_data,
            'total': len(sessions_data)
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting sessions: {e}")
        return jsonify({'error': str(e)}), 500
