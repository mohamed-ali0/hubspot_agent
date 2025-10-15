# HubSpot Logging AI Agent

AI-powered WhatsApp chatbot that analyzes conversations and automatically logs activities to HubSpot CRM.

## Features

- **WhatsApp Integration**: Receives and processes WhatsApp messages
- **AI Message Analysis**: Automatically detects contacts, deals, tasks, and notes in conversations
- **HubSpot Integration**: Seamlessly syncs data to HubSpot CRM
- **Session Management**: Organizes conversations into manageable sessions
- **Real-time Analytics**: Provides insights into sales activities and sync status
- **RESTful API**: Complete API for managing users, sessions, messages, and logs

## Quick Start

### 1. Installation

```bash
# Clone the repository
git clone <repository-url>
cd hubspot-logging-api

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp env.example .env
# Edit .env with your configuration

# Initialize database
python scripts/init_db.py

# Seed test data (optional)
python scripts/seed_data.py
```

### 2. Configuration

Create a `.env` file with your settings:

```env
# Flask Configuration
SECRET_KEY=your-secret-key-here
FLASK_ENV=development

# Database
DATABASE_URL=sqlite:///data/database.db

# HubSpot API
HUBSPOT_API_URL=https://api.hubapi.com
HUBSPOT_ACCESS_TOKEN=your-hubspot-access-token

# JWT Configuration
JWT_SECRET_KEY=your-jwt-secret-key
JWT_ACCESS_TOKEN_EXPIRES=3600
```

### 3. Run the Application

```bash
# Development mode
python app/main.py

# Or use Flask CLI
export FLASK_APP=app.main:app
flask run
```

The API will be available at `http://localhost:5000`

## API Documentation

### Authentication

#### Login
```http
POST /api/auth/login
Content-Type: application/json

{
  "username": "johndoe",
  "password": "password123"
}
```

Response:
```json
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "user": {
    "id": 1,
    "name": "John Doe",
    "username": "johndoe",
    "phone_number": "+1234567890"
  }
}
```

#### Get Current User
```http
GET /api/auth/me
Authorization: Bearer <token>
```

### Sessions

#### Create Session
```http
POST /api/sessions
Authorization: Bearer <token>
Content-Type: application/json

{
  "user_id": 1
}
```

#### Get Sessions
```http
GET /api/sessions?status=active&limit=20&offset=0
Authorization: Bearer <token>
```

#### Close Session
```http
PATCH /api/sessions/{session_id}/close
Authorization: Bearer <token>
```

### Messages

#### Create Message
```http
POST /api/sessions/{session_id}/messages
Authorization: Bearer <token>
Content-Type: application/json

{
  "message_text": "Had a great call with Ahmed from XYZ Corp...",
  "forwarded_from": "+201234567890",
  "timestamp": "2025-01-15T10:30:00Z"
}
```

#### Get Messages
```http
GET /api/sessions/{session_id}/messages?limit=50&order=desc
Authorization: Bearer <token>
```

### Logs (HubSpot Activities)

#### Create Log
```http
POST /api/logs
Authorization: Bearer <token>
Content-Type: application/json

{
  "session_id": 1,
  "chat_message_id": 5,
  "log_type": "note",
  "hubspot_payload": {
    "properties": {
      "hs_note_body": "Client meeting notes..."
    }
  }
}
```

#### Get Logs
```http
GET /api/logs?log_type=note&sync_status=synced&limit=50
Authorization: Bearer <token>
```

### HubSpot Integration

#### Create Contact
```http
POST /api/hubspot/contacts
Authorization: Bearer <token>
Content-Type: application/json

{
  "session_id": 1,
  "chat_message_id": 5,
  "properties": {
    "firstname": "Ahmed",
    "lastname": "Ali",
    "email": "ahmed@example.com",
    "phone": "+201234567890"
  }
}
```

#### Create Deal
```http
POST /api/hubspot/deals
Authorization: Bearer <token>
Content-Type: application/json

{
  "session_id": 1,
  "chat_message_id": 5,
  "properties": {
    "dealname": "XYZ Corp - Premium Package",
    "amount": "50000",
    "dealstage": "qualifiedtobuy"
  }
}
```

#### Create Note
```http
POST /api/hubspot/notes
Authorization: Bearer <token>
Content-Type: application/json

{
  "session_id": 1,
  "chat_message_id": 5,
  "properties": {
    "hs_note_body": "Discussed pricing and timeline..."
  },
  "associations": {
    "contacts": ["12345"],
    "deals": ["67890"]
  }
}
```

### Analytics

#### Get Overview Stats
```http
GET /api/stats/overview?start_date=2025-01-01&end_date=2025-01-31
Authorization: Bearer <token>
```

Response:
```json
{
  "total_sessions": 50,
  "active_sessions": 3,
  "total_messages": 500,
  "total_logs": 150,
  "logs_by_type": {
    "note": 60,
    "task": 30,
    "deal": 20
  },
  "sync_stats": {
    "pending": 5,
    "synced": 140,
    "failed": 5
  }
}
```

## WhatsApp Integration

The system is designed to work with WhatsApp Business API or webhook integrations. Messages received from WhatsApp are:

1. **Analyzed** by the AI service for actionable content
2. **Categorized** into contacts, deals, notes, or tasks
3. **Automatically synced** to HubSpot CRM

### Message Analysis

The AI service detects:
- **Contacts**: Client mentions, phone numbers, email addresses
- **Deals**: Pricing discussions, budget mentions, opportunities
- **Notes**: Meeting summaries, conversation details
- **Tasks**: Follow-up actions, reminders, scheduled activities

## Database Schema

### Users
Sales representatives who use the system

### Chat Sessions
Organized conversation threads

### Chat Messages
Individual messages within sessions

### Logs
HubSpot activities created from messages

## Development

### Running Tests
```bash
pytest tests/
```

### Database Migration
```bash
flask db migrate -m "description"
flask db upgrade
```

### Adding New Features

1. **New Models**: Add to `app/models/`
2. **API Endpoints**: Add to `app/api/v1/`
3. **Business Logic**: Add to `app/services/`
4. **Tests**: Add to `tests/`

## Deployment

### Production Setup
1. Set `FLASK_ENV=production`
2. Configure production database
3. Set secure SECRET_KEY and JWT_SECRET_KEY
4. Configure HubSpot production credentials
5. Use a production WSGI server (Gunicorn, etc.)

### Docker Deployment
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN python scripts/init_db.py

EXPOSE 5000
CMD ["python", "app/main.py"]
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## License

MIT License - see LICENSE file for details
