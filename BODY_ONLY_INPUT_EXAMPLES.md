# Body-Only Input Format Examples

## Overview
All API endpoints now accept ALL parameters in the request body. No query parameters are used.

## Key Changes

### ❌ **Before (Mixed Body + Query Parameters):**
```bash
curl -X GET "http://127.0.0.1:5000/api/hubspot/companies/companies?limit=5&properties=name,domain" \
  -H "Content-Type: application/json" \
  -d '{"token": "your_token"}'
```

### ✅ **After (Body-Only Parameters):**
```bash
curl -X GET http://127.0.0.1:5000/api/hubspot/companies/companies \
  -H "Content-Type: application/json" \
  -d '{
    "token": "your_token",
    "limit": 5,
    "properties": ["name", "domain"]
  }'
```

## API Usage Examples

### 1. GET Companies (Body-Only)
```bash
curl -X GET http://127.0.0.1:5000/api/hubspot/companies/companies \
  -H "Content-Type: application/json" \
  -d '{
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "limit": 5,
    "properties": ["name", "domain", "industry"]
  }'
```

**Request Body:**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "limit": 5,
  "properties": ["name", "domain", "industry"]
}
```

### 2. GET Specific Company (Body-Only)
```bash
curl -X GET http://127.0.0.1:5000/api/hubspot/companies/companies/123456789 \
  -H "Content-Type: application/json" \
  -d '{
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }'
```

**Request Body:**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### 3. SEARCH Companies (Body-Only)
```bash
curl -X POST http://127.0.0.1:5000/api/hubspot/companies/companies/search \
  -H "Content-Type: application/json" \
  -d '{
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "session_id": 1,
    "chat_message_id": 1,
    "search_term": "HubSpot",
    "limit": 10
  }'
```

**Request Body:**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "session_id": 1,
  "chat_message_id": 1,
  "search_term": "HubSpot",
  "limit": 10
}
```

### 4. CREATE Company (Body-Only)
```bash
curl -X POST http://127.0.0.1:5000/api/hubspot/companies/companies \
  -H "Content-Type: application/json" \
  -d '{
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "session_id": 1,
    "chat_message_id": 1,
    "properties": {
      "name": "New Company",
      "domain": "newcompany.com",
      "industry": "TECHNOLOGY",
      "phone": "+1-555-0123"
    }
  }'
```

**Request Body:**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "session_id": 1,
  "chat_message_id": 1,
  "properties": {
    "name": "New Company",
    "domain": "newcompany.com",
    "industry": "TECHNOLOGY",
    "phone": "+1-555-0123"
  }
}
```

### 5. UPDATE Company (Body-Only)
```bash
curl -X PATCH http://127.0.0.1:5000/api/hubspot/companies/companies/123456789 \
  -H "Content-Type: application/json" \
  -d '{
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "session_id": 1,
    "chat_message_id": 1,
    "properties": {
      "name": "Updated Company Name",
      "phone": "+1-555-9999"
    }
  }'
```

**Request Body:**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "session_id": 1,
  "chat_message_id": 1,
  "properties": {
    "name": "Updated Company Name",
    "phone": "+1-555-9999"
  }
}
```

### 6. DELETE Company (Body-Only)
```bash
curl -X DELETE http://127.0.0.1:5000/api/hubspot/companies/companies/123456789 \
  -H "Content-Type: application/json" \
  -d '{
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "session_id": 1,
    "chat_message_id": 1
  }'
```

**Request Body:**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "session_id": 1,
  "chat_message_id": 1
}
```

## Python Examples

### Using requests library
```python
import requests

# Get token
login_response = requests.post('http://127.0.0.1:5000/api/auth/login', 
                              json={'username': 'test', 'password': 'test'})
token = login_response.json()['token']

# GET Companies - ALL parameters in body
companies_data = {
    'token': token,
    'limit': 5,
    'properties': ['name', 'domain', 'industry']
}
response = requests.get(
    'http://127.0.0.1:5000/api/hubspot/companies/companies',
    json=companies_data  # No query parameters
)

# SEARCH Companies - ALL parameters in body
search_data = {
    'token': token,
    'session_id': 1,
    'chat_message_id': 1,
    'search_term': 'HubSpot',
    'limit': 10
}
response = requests.post(
    'http://127.0.0.1:5000/api/hubspot/companies/companies/search',
    json=search_data  # No query parameters
)

# CREATE Company - ALL parameters in body
create_data = {
    'token': token,
    'session_id': 1,
    'chat_message_id': 1,
    'properties': {
        'name': 'New Company',
        'domain': 'newcompany.com',
        'industry': 'TECHNOLOGY'
    }
}
response = requests.post(
    'http://127.0.0.1:5000/api/hubspot/companies/companies',
    json=create_data  # No query parameters
)
```

## JavaScript Examples

### Using fetch API
```javascript
// Get token
const loginResponse = await fetch('http://127.0.0.1:5000/api/auth/login', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({username: 'test', password: 'test'})
});
const {token} = await loginResponse.json();

// GET Companies - ALL parameters in body
const companiesResponse = await fetch(
  'http://127.0.0.1:5000/api/hubspot/companies/companies',
  {
    method: 'GET',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
      token,
      limit: 5,
      properties: ['name', 'domain', 'industry']
    })
  }
);

// SEARCH Companies - ALL parameters in body
const searchData = {
  token,
  session_id: 1,
  chat_message_id: 1,
  search_term: 'HubSpot',
  limit: 10
};

const searchResponse = await fetch(
  'http://127.0.0.1:5000/api/hubspot/companies/companies/search',
  {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(searchData)
  }
);
```

## Benefits

1. **Consistent Format**: All parameters in JSON body
2. **No URL Encoding**: No need to encode special characters in URLs
3. **Simpler Integration**: One JSON object for all parameters
4. **Better Logging**: All parameters logged together
5. **Easier Testing**: All data in request body

## Schema Definitions

### CompanyGetSchema
```json
{
  "token": "string (required)",
  "limit": "integer (optional, default: 10)",
  "properties": "array of strings (optional, default: [])"
}
```

### CompanySearchSchema
```json
{
  "token": "string (required)",
  "session_id": "integer (required)",
  "chat_message_id": "integer (required)",
  "search_term": "string (required)",
  "limit": "integer (optional, default: 10)"
}
```

### CompanyCreateSchema
```json
{
  "token": "string (required)",
  "session_id": "integer (required)",
  "chat_message_id": "integer (required)",
  "properties": "object (required)"
}
```

## Error Handling

### Missing Required Fields
```json
{
  "error": "Validation error",
  "details": {
    "token": ["Missing data for required field."]
  }
}
```

### Invalid Field Types
```json
{
  "error": "Validation error",
  "details": {
    "limit": ["Not a valid integer."]
  }
}
```
