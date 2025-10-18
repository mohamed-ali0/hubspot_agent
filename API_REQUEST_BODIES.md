# API Request Bodies Documentation

This document contains all the request body formats for the HubSpot Logging AI Agent API endpoints.

## Authentication

All endpoints require a JWT token in the request body.

### Get Token
```bash
POST /api/auth/login
```

**Request Body:**
```json
{
  "username": "test",
  "password": "test"
}
```

**Response:**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": 1,
    "username": "test",
    "email": "test@example.com"
  }
}
```

## Company Endpoints

### 1. Get All Companies
```bash
POST /api/hubspot/companies/companies
```

**Request Body:**
```json
{
  "token": "YOUR_JWT_TOKEN",
  "session_id": 1,
  "chat_message_id": 1,
  "limit": 10,
  "properties": ["name", "domain", "industry"]
}
```

### 2. Get Specific Company
```bash
POST /api/hubspot/companies/companies/get
```

**Request Body:**
```json
{
  "token": "YOUR_JWT_TOKEN",
  "company_id": "264244139217",
  "session_id": 1,
  "chat_message_id": 1
}
```

### 3. Create Company
```bash
POST /api/hubspot/companies/companies
```

**Request Body:**
```json
{
  "token": "YOUR_JWT_TOKEN",
  "session_id": 1,
  "chat_message_id": 1,
  "properties": {
    "name": "Test Company",
    "domain": "testcompany.com",
    "industry": "COMPUTER_SOFTWARE",
    "city": "New York",
    "state": "NY",
    "country": "USA",
    "phone": "+1234567890",
    "website": "https://testcompany.com",
    "description": "A test company for API testing"
  }
}
```

**Required Fields:**
- `token`: JWT authentication token
- `session_id`: Chat session ID (integer)
- `chat_message_id`: Chat message ID (integer)  
- `properties`: Object containing company properties

**Optional Company Properties:**
- `name`: Company name (string)
- `domain`: Company domain (string)
- `industry`: Industry type (string)
- `city`: City (string)
- `state`: State/Province (string)
- `country`: Country (string)
- `phone`: Phone number (string)
- `website`: Website URL (string)
- `description`: Company description (string)
- `address`: Street address (string)
- `zip`: Postal code (string)
- `numberofemployees`: Number of employees (integer)

### 4. Update Company
```bash
POST /api/hubspot/companies/companies/update
```

**Request Body:**
```json
{
  "token": "YOUR_JWT_TOKEN",
  "company_id": "264244139217",
  "session_id": 1,
  "chat_message_id": 1,
  "properties": {
    "name": "Updated Company Name",
    "industry": "TECHNOLOGY"
  }
}
```

### 5. Delete Company
```bash
POST /api/hubspot/companies/companies/delete
```

**Request Body:**
```json
{
  "token": "YOUR_JWT_TOKEN",
  "company_id": "264244139217",
  "session_id": 1,
  "chat_message_id": 1
}
```

### 6. Search Companies
```bash
POST /api/hubspot/companies/companies/search
```

**Request Body:**
```json
{
  "token": "YOUR_JWT_TOKEN",
  "session_id": 1,
  "chat_message_id": 1,
  "search_term": "test company",
  "limit": 10
}
```

### 7. Get Company Properties
```bash
POST /api/hubspot/companies/properties
```

**Request Body:**
```json
{
  "token": "YOUR_JWT_TOKEN",
  "session_id": 1,
  "chat_message_id": 1
}
```

### 8. Get Specific Company Property
```bash
POST /api/hubspot/companies/companies/properties/get
```

**Request Body:**
```json
{
  "token": "YOUR_JWT_TOKEN",
  "property_name": "name",
  "session_id": 1,
  "chat_message_id": 1
}
```

## Contact Endpoints

### 1. Get All Contacts
```bash
POST /api/hubspot/contacts/contacts
```

**Request Body:**
```json
{
  "token": "YOUR_JWT_TOKEN",
  "session_id": 1,
  "chat_message_id": 1,
  "limit": 10,
  "properties": ["firstname", "lastname", "email"]
}
```

### 2. Get Specific Contact
```bash
POST /api/hubspot/contacts/contacts/get
```

**Request Body:**
```json
{
  "token": "YOUR_JWT_TOKEN",
  "contact_id": "123456789",
  "session_id": 1,
  "chat_message_id": 1
}
```

### 3. Create Contact
```bash
POST /api/hubspot/contacts/contacts
```

**Request Body:**
```json
{
  "token": "YOUR_JWT_TOKEN",
  "session_id": 1,
  "chat_message_id": 1,
  "properties": {
    "firstname": "John",
    "lastname": "Doe",
    "email": "john.doe@example.com",
    "phone": "+1234567890",
    "company": "Test Company",
    "jobtitle": "Software Engineer",
    "city": "New York",
    "state": "NY",
    "country": "USA",
    "website": "https://johndoe.com",
    "lifecyclestage": "lead"
  }
}
```

**Required Fields:**
- `token`: JWT authentication token
- `session_id`: Chat session ID (integer)
- `chat_message_id`: Chat message ID (integer)
- `properties`: Object containing contact properties

**Optional Contact Properties:**
- `firstname`: First name (string)
- `lastname`: Last name (string)
- `email`: Email address (string)
- `phone`: Phone number (string)
- `company`: Company name (string)
- `jobtitle`: Job title (string)
- `city`: City (string)
- `state`: State/Province (string)
- `country`: Country (string)
- `website`: Website URL (string)
- `lifecyclestage`: Lifecycle stage (string) - lead, marketingqualifiedlead, salesqualifiedlead, opportunity, customer, evangelist, subscriber, other
- `leadstatus`: Lead status (string)
- `hs_lead_status`: HubSpot lead status (string)

### 4. Update Contact
```bash
POST /api/hubspot/contacts/contacts/update
```

**Request Body:**
```json
{
  "token": "YOUR_JWT_TOKEN",
  "contact_id": "123456789",
  "session_id": 1,
  "chat_message_id": 1,
  "properties": {
    "firstname": "Jane",
    "lastname": "Smith"
  }
}
```

### 5. Delete Contact
```bash
POST /api/hubspot/contacts/contacts/delete
```

**Request Body:**
```json
{
  "token": "YOUR_JWT_TOKEN",
  "contact_id": "123456789",
  "session_id": 1,
  "chat_message_id": 1
}
```

## Deal Endpoints

### 1. Get All Deals
```bash
POST /api/hubspot/deals/deals
```

**Request Body:**
```json
{
  "token": "YOUR_JWT_TOKEN",
  "session_id": 1,
  "chat_message_id": 1,
  "limit": 10,
  "properties": ["dealname", "amount", "dealstage"]
}
```

### 2. Create Deal
```bash
POST /api/hubspot/deals/deals
```

**Request Body:**
```json
{
  "token": "YOUR_JWT_TOKEN",
  "session_id": 1,
  "chat_message_id": 1,
  "properties": {
    "dealname": "Test Deal",
    "amount": "50000",
    "dealstage": "appointmentscheduled",
    "pipeline": "default"
  }
}
```

### 3. Update Deal
```bash
POST /api/hubspot/deals/deals/update
```

**Request Body:**
```json
{
  "token": "YOUR_JWT_TOKEN",
  "deal_id": "123456789",
  "session_id": 1,
  "chat_message_id": 1,
  "properties": {
    "dealname": "Updated Deal Name",
    "amount": "75000"
  }
}
```

## Task Endpoints

### 1. Create Task
```bash
POST /api/hubspot/tasks/tasks
```

**Request Body:**
```json
{
  "token": "YOUR_JWT_TOKEN",
  "session_id": 1,
  "chat_message_id": 1,
  "properties": {
    "hs_task_subject": "Follow up with client",
    "hs_task_status": "NOT_STARTED",
    "hs_task_priority": "HIGH",
    "hs_task_type": "CALL"
  }
}
```

### 2. Update Task
```bash
POST /api/hubspot/tasks/tasks/update
```

**Request Body:**
```json
{
  "token": "YOUR_JWT_TOKEN",
  "task_id": "123456789",
  "session_id": 1,
  "chat_message_id": 1,
  "properties": {
    "hs_task_status": "COMPLETED"
  }
}
```

## Meeting Endpoints

### 1. Create Meeting
```bash
POST /api/hubspot/activities/meetings
```

**Request Body:**
```json
{
  "token": "YOUR_JWT_TOKEN",
  "session_id": 1,
  "chat_message_id": 1,
  "properties": {
    "hs_meeting_title": "Client Meeting",
    "hs_meeting_body": "Discuss project requirements",
    "hs_meeting_start_time": "2025-01-20T10:00:00Z",
    "hs_meeting_end_time": "2025-01-20T11:00:00Z"
  }
}
```

## Call Endpoints

### 1. Create Call
```bash
POST /api/hubspot/activities/calls
```

**Request Body:**
```json
{
  "token": "YOUR_JWT_TOKEN",
  "session_id": 1,
  "chat_message_id": 1,
  "properties": {
    "hs_call_title": "Client Call",
    "hs_call_body": "Follow up call with client",
    "hs_call_duration": "1800",
    "hs_call_outcome": "COMPLETED"
  }
}
```

## Note Endpoints

### 1. Create Note
```bash
POST /api/hubspot/notes/notes
```

**Request Body:**
```json
{
  "token": "YOUR_JWT_TOKEN",
  "session_id": 1,
  "chat_message_id": 1,
  "properties": {
    "hs_note_body": "This is a test note about the client meeting."
  }
}
```

## Lead Endpoints

### 1. Create Lead
```bash
POST /api/hubspot/leads/leads
```

**Request Body:**
```json
{
  "token": "YOUR_JWT_TOKEN",
  "session_id": 1,
  "chat_message_id": 1,
  "properties": {
    "firstname": "John",
    "lastname": "Doe",
    "email": "john.doe@example.com",
    "company": "Test Company",
    "phone": "+1234567890"
  }
}
```

### 2. Qualify Lead
```bash
POST /api/hubspot/leads/leads/qualify
```

**Request Body:**
```json
{
  "token": "YOUR_JWT_TOKEN",
  "lead_id": "123456789",
  "session_id": 1,
  "chat_message_id": 1,
  "deal_properties": {
    "dealname": "Qualified Lead Deal",
    "amount": "25000",
    "dealstage": "appointmentscheduled"
  }
}
```

## Association Endpoints

### 1. Create Contact-Deal Association
```bash
POST /api/hubspot/associations/associations/contact-deal
```

**Request Body:**
```json
{
  "token": "YOUR_JWT_TOKEN",
  "session_id": 1,
  "chat_message_id": 1,
  "contact_id": "123456789",
  "deal_id": "987654321"
}
```

### 2. Create Contact-Company Association
```bash
POST /api/hubspot/associations/associations/contact-company
```

**Request Body:**
```json
{
  "token": "YOUR_JWT_TOKEN",
  "session_id": 1,
  "chat_message_id": 1,
  "contact_id": "123456789",
  "company_id": "456789123"
}
```

## Complete Request Body Structure

### Standard Request Body Format
All API endpoints follow this structure:

```json
{
  "token": "YOUR_JWT_TOKEN",
  "session_id": 1,
  "chat_message_id": 1,
  "additional_fields": "as_needed"
}
```

### Required Fields (All Endpoints)
- `token`: JWT authentication token (string) - Get from `/api/auth/login`
- `session_id`: Chat session ID (integer) - Use 1 for testing
- `chat_message_id`: Chat message ID (integer) - Use 1 for testing

### Optional Fields (Varies by Endpoint)
- `limit`: Number of records to return (integer, default: 10)
- `properties`: Object containing data properties (for create/update operations)
- `search_term`: Search query for search endpoints (string)
- `company_id`: Company ID for company-specific operations (string)
- `contact_id`: Contact ID for contact-specific operations (string)
- `deal_id`: Deal ID for deal-specific operations (string)
- `task_id`: Task ID for task-specific operations (string)
- `property_name`: Property name for property-specific operations (string)

### Properties Object Structure
For create/update operations, the `properties` object contains the actual data:

```json
{
  "properties": {
    "field1": "value1",
    "field2": "value2",
    "field3": "value3"
  }
}
```

### Data Types
- **String**: Text values (e.g., "John Doe", "test@example.com")
- **Integer**: Numeric values (e.g., 1, 100, 50000)
- **Boolean**: True/false values (e.g., true, false)
- **Array**: List of values (e.g., ["value1", "value2"])
- **Object**: Nested JSON object for complex data

## Valid Test IDs

Based on your database:
- **Session ID**: `1`
- **Message ID**: `1`
- **User ID**: `1`

## Example cURL Commands

### Delete Company
```bash
curl -X POST http://127.0.0.1:5000/api/hubspot/companies/companies/delete \
  -H "Content-Type: application/json" \
  -d '{
    "token": "YOUR_JWT_TOKEN",
    "company_id": "264244139217",
    "session_id": 1,
    "chat_message_id": 1
  }'
```

### Create Company
```bash
curl -X POST http://127.0.0.1:5000/api/hubspot/companies/companies \
  -H "Content-Type: application/json" \
  -d '{
    "token": "YOUR_JWT_TOKEN",
    "session_id": 1,
    "chat_message_id": 1,
    "properties": {
      "name": "Test Company",
      "domain": "testcompany.com",
      "industry": "COMPUTER_SOFTWARE"
    }
  }'
```

## Notes

1. All endpoints use POST method with JSON body
2. All parameters are in the request body, not URL parameters
3. JWT tokens expire after 1 hour
4. Use the provided test IDs for testing
5. HubSpot API keys are stored securely in the database
6. All operations are logged to the local database
