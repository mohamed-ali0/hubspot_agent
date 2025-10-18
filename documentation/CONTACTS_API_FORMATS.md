# Contacts API Request Formats

## Overview
All contacts endpoints use body-based authentication and accept stringified JSON for the `properties` field.

## Endpoints

### 1. Create Contact
- **URL**: `POST /api/hubspot/contacts/contacts`
- **Method**: POST
- **Request Body**:
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "session_id": 1,
  "chat_message_id": 1,
  "properties": "{\"firstname\":\"John\",\"lastname\":\"Doe\",\"email\":\"john.doe@example.com\",\"phone\":\"+1234567890\",\"company\":\"Test Company\",\"jobtitle\":\"Software Engineer\",\"city\":\"New York\",\"state\":\"NY\",\"country\":\"USA\",\"lifecyclestage\":\"lead\"}"
}
```

### 2. Get All Contacts
- **URL**: `POST /api/hubspot/contacts/contacts/get`
- **Method**: POST
- **Request Body**:
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "session_id": 1,
  "chat_message_id": 1,
  "limit": 5,
  "properties": ["firstname", "lastname", "email"]
}
```

### 3. Get Specific Contact
- **URL**: `POST /api/hubspot/contacts/contacts/get-by-id`
- **Method**: POST
- **Request Body**:
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "contact_id": "488649095384",
  "session_id": 1,
  "chat_message_id": 1
}
```

### 4. Update Contact
- **URL**: `POST /api/hubspot/contacts/contacts/update`
- **Method**: POST
- **Request Body**:
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "contact_id": "488649095384",
  "session_id": 1,
  "chat_message_id": 1,
  "properties": "{\"firstname\":\"Jane\",\"lastname\":\"Smith\",\"jobtitle\":\"Senior Software Engineer\",\"city\":\"San Francisco\",\"state\":\"CA\"}"
}
```

### 5. Search Contacts
- **URL**: `POST /api/hubspot/contacts/contacts/search`
- **Method**: POST
- **Request Body**:
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "session_id": 1,
  "chat_message_id": 1,
  "search_term": "John",
  "limit": 5
}
```

### 6. Delete Contact
- **URL**: `POST /api/hubspot/contacts/contacts/delete`
- **Method**: POST
- **Request Body**:
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "contact_id": "488649095384",
  "session_id": 1,
  "chat_message_id": 1
}
```

## Key Features

1. **Body-based Authentication**: All endpoints require the JWT token in the request body
2. **Stringified JSON Support**: The `properties` field can be either a JSON object or a stringified JSON
3. **Consistent Logging**: All operations are logged to the database with session and message IDs
4. **Error Handling**: Comprehensive error handling with detailed error messages

## Common Contact Properties

- `firstname`: Contact's first name
- `lastname`: Contact's last name
- `email`: Contact's email address (unique identifier)
- `phone`: Contact's phone number
- `company`: Company name
- `jobtitle`: Job title
- `city`: City
- `state`: State/Province
- `country`: Country
- `lifecyclestage`: Lead stage (lead, customer, etc.)
- `website`: Website URL
- `industry`: Industry type

## Response Format

All successful operations return:
```json
{
  "message": "Operation completed successfully",
  "hubspot_id": "488649095384",
  "data": { ... }
}
```

Error responses return:
```json
{
  "error": "Error message description"
}
```
