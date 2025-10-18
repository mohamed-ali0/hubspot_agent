# Twilio WhatsApp Integration Setup Guide

## Prerequisites
- Twilio Account (https://www.twilio.com/)
- WhatsApp Business Account
- ngrok (for local development)
- Your Flask API running

## Step 1: Twilio Account Setup

### 1.1 Create Twilio Account
1. Go to https://www.twilio.com/
2. Sign up for a free account
3. Verify your phone number
4. Complete account setup

### 1.2 Get Twilio Credentials
1. Go to Console Dashboard
2. Note down:
   - **Account SID** (starts with AC...)
   - **Auth Token** (click to reveal)
   - **Phone Number** (from Phone Numbers > Manage > Active numbers)

## Step 2: WhatsApp Business API Setup

### 2.1 Request WhatsApp Business API Access
1. Go to Twilio Console > Messaging > Try it out > Send a WhatsApp message
2. Click "Get started with WhatsApp"
3. Follow the verification process:
   - Provide business information
   - Verify your business phone number
   - Wait for approval (can take 24-48 hours)

### 2.2 Configure WhatsApp Sandbox (for testing)
1. Go to Messaging > Try it out > Send a WhatsApp message
2. Click "Sandbox" tab
3. Note the sandbox number (e.g., +1 415 523 8886)
4. Send the join code to your WhatsApp number
5. You'll receive a confirmation message

## Step 3: Environment Configuration

### 3.1 Update .env file
Add these variables to your `.env` file:

```env
# Twilio Configuration
TWILIO_ACCOUNT_SID=your_account_sid_here
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_WHATSAPP_NUMBER=+14155238886
TWILIO_WEBHOOK_URL=https://your-ngrok-url.ngrok.io/api/whatsapp/webhook

# WhatsApp Configuration
WHATSAPP_WEBHOOK_VERIFY_TOKEN=your_webhook_verify_token
```

### 3.2 Install Twilio Python SDK
```bash
pip install twilio
```

## Step 4: Update WhatsApp Controller

### 4.1 Add Twilio Integration
Update `app/api/v1/whatsapp.py` to include Twilio sending:

```python
from twilio.rest import Client
import os

# Initialize Twilio client
def get_twilio_client():
    account_sid = os.getenv('TWILIO_ACCOUNT_SID')
    auth_token = os.getenv('TWILIO_AUTH_TOKEN')
    return Client(account_sid, auth_token)

@bp.route('/send', methods=['POST'])
@jwt_required()
def send_message():
    """Send WhatsApp message via Twilio"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        to_number = data.get('to')
        message_text = data.get('message')
        session_id = data.get('session_id')
        message_id = data.get('message_id')
        
        if not all([to_number, message_text]):
            return jsonify({'error': 'Missing required fields: to, message'}), 400
        
        # Send via Twilio
        client = get_twilio_client()
        whatsapp_number = os.getenv('TWILIO_WHATSAPP_NUMBER')
        
        message = client.messages.create(
            body=message_text,
            from_=f'whatsapp:{whatsapp_number}',
            to=f'whatsapp:{to_number}'
        )
        
        # Log the outgoing message
        _create_log(
            user_id=current_user_id,
            session_id=session_id or 0,
            message_id=message_id or 0,
            log_type='whatsapp_send',
            hubspot_id=message.sid,
            sync_status='synced'
        )
        
        return jsonify({
            'status': 'success',
            'message_sid': message.sid,
            'to': to_number,
            'text': message_text
        }), 200
        
    except Exception as e:
        logger.error(f"Error sending WhatsApp message: {e}")
        return jsonify({'error': str(e)}), 500
```

## Step 5: Local Development Setup

### 5.1 Install ngrok
```bash
# Download from https://ngrok.com/download
# Or install via package manager
npm install -g ngrok
# or
brew install ngrok
```

### 5.2 Start your Flask app
```bash
cd app
python main.py
```

### 5.3 Expose your app with ngrok
```bash
ngrok http 5000
```

Copy the HTTPS URL (e.g., `https://abc123.ngrok.io`)

### 5.4 Configure Twilio Webhook
1. Go to Twilio Console > Phone Numbers > Manage > Active numbers
2. Click on your WhatsApp number
3. In the "Messaging" section:
   - **Webhook URL**: `https://your-ngrok-url.ngrok.io/api/whatsapp/webhook`
   - **HTTP Method**: POST
   - **Save Configuration**

## Step 6: n8n Integration Setup

### 6.1 Create n8n Workflow
1. **Webhook Node** (Start):
   - Method: POST
   - Path: `/whatsapp-webhook`
   - Response: JSON

2. **Chat Node** (AI Processing):
   - Connect to your AI service
   - Process incoming message
   - Determine HubSpot actions needed

3. **HTTP Request Node** (Call your API):
   - Method: POST
   - URL: `http://your-flask-app/api/hubspot/contacts/contacts`
   - Headers: `Authorization: Bearer {token}`
   - Body: JSON with session_id, chat_message_id, properties

4. **Twilio Node** (Send Response):
   - Send AI response back to user

### 6.2 n8n Workflow Example
```json
{
  "nodes": [
    {
      "name": "WhatsApp Webhook",
      "type": "n8n-nodes-base.webhook",
      "parameters": {
        "httpMethod": "POST",
        "path": "whatsapp-webhook"
      }
    },
    {
      "name": "AI Chat",
      "type": "n8n-nodes-base.openAi",
      "parameters": {
        "resource": "chat",
        "model": "gpt-3.5-turbo",
        "messages": "{{ $json.messages }}"
      }
    },
    {
      "name": "Call HubSpot API",
      "type": "n8n-nodes-base.httpRequest",
      "parameters": {
        "method": "POST",
        "url": "http://localhost:5000/api/hubspot/contacts/contacts",
        "headers": {
          "Authorization": "Bearer YOUR_JWT_TOKEN",
          "Content-Type": "application/json"
        },
        "body": {
          "session_id": "{{ $json.session_id }}",
          "chat_message_id": "{{ $json.message_id }}",
          "properties": {
            "firstname": "{{ $json.firstname }}",
            "lastname": "{{ $json.lastname }}",
            "email": "{{ $json.email }}",
            "phone": "{{ $json.phone }}"
          }
        }
      }
    }
  ]
}
```

## Step 7: Testing

### 7.1 Test Webhook
```bash
curl -X POST https://your-ngrok-url.ngrok.io/api/whatsapp/webhook \
  -H "Content-Type: application/json" \
  -d '{
    "entry": [{
      "changes": [{
        "value": {
          "messages": [{
            "id": "test123",
            "from": "+1234567890",
            "text": {"body": "Hello, I want to create a contact"},
            "timestamp": "1640995200"
          }]
        }
      }]
    }]
  }'
```

### 7.2 Test Send Message
```bash
curl -X POST http://localhost:5000/api/whatsapp/send \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "+1234567890",
    "message": "Hello from your AI agent!",
    "session_id": 1,
    "message_id": 1
  }'
```

## Step 8: Production Deployment

### 8.1 Update Webhook URL
1. Deploy your Flask app to production
2. Update Twilio webhook URL to your production domain
3. Update environment variables with production values

### 8.2 SSL Certificate
- Ensure your production server has SSL certificate
- Twilio requires HTTPS for webhooks

## Troubleshooting

### Common Issues:
1. **Webhook not receiving messages**: Check ngrok URL and Twilio configuration
2. **Authentication errors**: Verify JWT tokens and user setup
3. **Message sending fails**: Check Twilio credentials and WhatsApp sandbox setup
4. **AI not responding**: Verify n8n workflow and API connections

### Debug Commands:
```bash
# Check webhook status
curl https://your-ngrok-url.ngrok.io/api/whatsapp/status

# View logs
tail -f app.log

# Test Twilio connection
python -c "from twilio.rest import Client; print(Client('AC...', '...').messages.list())"
```

## Security Considerations

1. **Webhook Verification**: Implement Twilio signature verification
2. **Rate Limiting**: Add rate limiting to prevent abuse
3. **Input Validation**: Validate all incoming data
4. **Error Handling**: Implement comprehensive error handling
5. **Logging**: Log all activities for audit trail

## Next Steps

1. Set up Twilio account and get credentials
2. Configure WhatsApp sandbox
3. Update your .env file
4. Test the webhook endpoint
5. Create n8n workflow
6. Test end-to-end flow
7. Deploy to production

Your WhatsApp integration is now ready to receive messages, process them with AI, and execute HubSpot actions!
