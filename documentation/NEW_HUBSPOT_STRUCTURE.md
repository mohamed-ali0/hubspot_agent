# New HubSpot API Structure

## Overview

The HubSpot API has been reorganized into a clean, object-oriented structure where each HubSpot object type has its own dedicated file with complete CRUD operations and logging.

## New File Structure

```
app/api/v1/hubspot/
├── __init__.py              # Package initialization
├── contacts.py              # Contact operations
├── companies.py             # Company operations  
├── deals.py                 # Deal operations
├── notes.py                 # Note operations
├── tasks.py                 # Task operations
├── activities.py            # Calls, meetings, emails
└── associations.py          # Object associations
```

## API Endpoints

### Contacts API (`/api/hubspot/contacts/`)

**GET Operations:**
- `GET /contacts` - Get all contacts
- `GET /contacts/{id}` - Get specific contact
- `GET /contacts/search` - Search contacts
- `GET /contacts/properties` - Get contact properties
- `GET /contacts/properties/{name}` - Get specific property

**POST Operations:**
- `POST /contacts` - Create contact
- `POST /contacts/batch` - Batch create contacts
- `POST /contacts/search` - Search contacts

**UPDATE Operations:**
- `PATCH /contacts/{id}` - Update contact
- `PUT /contacts/{id}` - Replace contact
- `PATCH /contacts/batch` - Batch update contacts

**DELETE Operations:**
- `DELETE /contacts/{id}` - Delete contact

### Companies API (`/api/hubspot/companies/`)

**GET Operations:**
- `GET /companies` - Get all companies
- `GET /companies/{id}` - Get specific company
- `GET /companies/search` - Search companies
- `GET /companies/properties` - Get company properties
- `GET /companies/properties/{name}` - Get specific property

**POST Operations:**
- `POST /companies` - Create company
- `POST /companies/batch` - Batch create companies
- `POST /companies/search` - Search companies

**UPDATE Operations:**
- `PATCH /companies/{id}` - Update company
- `PUT /companies/{id}` - Replace company
- `PATCH /companies/batch` - Batch update companies

**DELETE Operations:**
- `DELETE /companies/{id}` - Delete company

### Deals API (`/api/hubspot/deals/`)

**GET Operations:**
- `GET /deals` - Get all deals
- `GET /deals/{id}` - Get specific deal
- `GET /deals/search` - Search deals
- `GET /deals/pipelines` - Get deal pipelines
- `GET /deals/pipelines/{id}/stages` - Get deal stages

**POST Operations:**
- `POST /deals` - Create deal
- `POST /deals/batch` - Batch create deals
- `POST /deals/search` - Search deals

**UPDATE Operations:**
- `PATCH /deals/{id}` - Update deal
- `PUT /deals/{id}` - Replace deal
- `PATCH /deals/batch` - Batch update deals

**DELETE Operations:**
- `DELETE /deals/{id}` - Delete deal

### Notes API (`/api/hubspot/notes/`)

**GET Operations:**
- `GET /notes` - Get all notes
- `GET /notes/{id}` - Get specific note
- `GET /notes/search` - Search notes
- `GET /notes/{id}/associations` - Get note associations

**POST Operations:**
- `POST /notes` - Create note
- `POST /notes/batch` - Batch create notes
- `POST /notes/search` - Search notes
- `POST /notes/{id}/associations` - Create note associations

**UPDATE Operations:**
- `PATCH /notes/{id}` - Update note
- `PUT /notes/{id}` - Replace note
- `PATCH /notes/batch` - Batch update notes

**DELETE Operations:**
- `DELETE /notes/{id}` - Delete note

### Tasks API (`/api/hubspot/tasks/`)

**GET Operations:**
- `GET /tasks` - Get all tasks
- `GET /tasks/{id}` - Get specific task
- `GET /tasks/search` - Search tasks

**POST Operations:**
- `POST /tasks` - Create task
- `POST /tasks/batch` - Batch create tasks
- `POST /tasks/search` - Search tasks

**UPDATE Operations:**
- `PATCH /tasks/{id}` - Update task
- `PUT /tasks/{id}` - Replace task
- `PATCH /tasks/batch` - Batch update tasks
- `PATCH /tasks/{id}/status` - Update task status
- `POST /tasks/{id}/complete` - Complete task

**DELETE Operations:**
- `DELETE /tasks/{id}` - Delete task

### Activities API (`/api/hubspot/activities/`)

**Calls:**
- `GET /calls` - Get all calls
- `GET /calls/{id}` - Get specific call
- `POST /calls` - Create call

**Meetings:**
- `GET /meetings` - Get all meetings
- `GET /meetings/{id}` - Get specific meeting
- `POST /meetings` - Create meeting

**Emails:**
- `GET /emails` - Get all emails
- `GET /emails/{id}` - Get specific email
- `POST /emails` - Create email

**Generic Activities:**
- `GET /activities` - Get all activities
- `POST /activities/search` - Search activities
- `PATCH /activities/{id}` - Update activity
- `DELETE /activities/{id}` - Delete activity

### Associations API (`/api/hubspot/associations/`)

**Association Management:**
- `POST /associations` - Create association
- `POST /associations/batch` - Batch create associations
- `GET /associations/{object_type}/{object_id}` - Get object associations
- `POST /associations/search` - Search associations
- `DELETE /associations/{from_type}/{from_id}/{to_type}/{to_id}` - Delete association

**Specific Associations:**
- `POST /associations/contact-deal` - Associate contact with deal
- `POST /associations/contact-company` - Associate contact with company
- `POST /associations/deal-company` - Associate deal with company

**Association Types:**
- `GET /associations/types` - Get all association types
- `GET /associations/types/{object_type}` - Get types for object

## Key Features

### 1. Complete CRUD Operations
Each object type has full Create, Read, Update, Delete operations:
- **Create**: POST endpoints with validation
- **Read**: GET endpoints with filtering and search
- **Update**: PATCH (partial) and PUT (replace) endpoints
- **Delete**: DELETE endpoints with confirmation

### 2. Batch Operations
All object types support batch operations:
- **Batch Create**: Create multiple objects at once
- **Batch Update**: Update multiple objects at once
- **Batch Delete**: Delete multiple objects at once

### 3. Advanced Features
- **Search**: Full-text search across all object types
- **Properties**: Schema and property management
- **Associations**: Link objects together
- **Activities**: Track calls, meetings, emails
- **Pipelines**: Deal pipeline and stage management

### 4. Comprehensive Logging
Every operation is logged to the database with:
- **User ID**: Who performed the action
- **Session ID**: Which chat session
- **Message ID**: Which message triggered the action
- **Log Type**: Type of operation (contact_action, deal, note, etc.)
- **HubSpot ID**: HubSpot record ID
- **Sync Status**: pending, synced, failed
- **Timestamps**: When the operation occurred

### 5. Request Validation
All endpoints use Marshmallow schemas for validation:
- **Required fields**: Validated before processing
- **Data types**: Automatic type conversion and validation
- **Error handling**: Clear error messages for validation failures

### 6. Authentication
All endpoints require JWT authentication:
- **Bearer token**: Required in Authorization header
- **User context**: Operations are tied to authenticated user
- **Security**: All operations are user-scoped

## Backward Compatibility

The original HubSpot endpoints (`/api/hubspot/`) are still available for backward compatibility:
- `GET /api/hubspot/contacts` - Legacy contacts endpoint
- `GET /api/hubspot/deals` - Legacy deals endpoint
- `GET /api/hubspot/notes` - Legacy notes endpoint
- `GET /api/hubspot/tasks` - Legacy tasks endpoint

## Usage Examples

### Create a Contact
```bash
POST /api/hubspot/contacts/contacts
{
  "session_id": 1,
  "chat_message_id": 5,
  "properties": {
    "firstname": "John",
    "lastname": "Doe",
    "email": "john@example.com"
  }
}
```

### Search Deals
```bash
POST /api/hubspot/deals/search
{
  "session_id": 1,
  "chat_message_id": 5,
  "search_term": "enterprise"
}
```

### Create Association
```bash
POST /api/hubspot/associations/contact-deal
{
  "contact_id": "12345",
  "deal_id": "67890",
  "session_id": 1,
  "chat_message_id": 5
}
```

### Batch Create Tasks
```bash
POST /api/hubspot/tasks/batch
{
  "session_id": 1,
  "chat_message_id": 5,
  "tasks": [
    {
      "properties": {
        "hs_task_subject": "Follow up call",
        "hs_task_body": "Call client next week"
      }
    }
  ]
}
```

## Testing

Use the test script to verify all endpoints:
```bash
python test_new_hubspot_structure.py
```

This will test all CRUD operations, batch operations, and logging functionality across all object types.

## Benefits

1. **Organization**: Each object type has its own file and endpoints
2. **Completeness**: Full CRUD operations for every object type
3. **Logging**: Every operation is logged to the database
4. **Validation**: Request validation with clear error messages
5. **Batch Operations**: Efficient bulk operations
6. **Search**: Full-text search capabilities
7. **Associations**: Link objects together
8. **Backward Compatibility**: Legacy endpoints still work
9. **Scalability**: Easy to add new object types
10. **Maintainability**: Clean, organized code structure
