# Body-Based JWT Authentication Examples

## Overview
All API endpoints now accept JWT tokens in the request body instead of the Authorization header.

## Authentication Flow

### 1. Get JWT Token
```bash
curl -X POST http://127.0.0.1:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "test", "password": "test"}'
```

**Response:**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "message": "Login successful"
}
```

## API Usage Examples

### 1. GET Companies
```bash
curl -X GET http://127.0.0.1:5000/api/hubspot/companies/companies \
  -H "Content-Type: application/json" \
  -d '{"token": "your_jwt_token"}' \
  --get --data-urlencode "limit=5" \
  --data-urlencode "properties=name,domain,industry"
```

**Request Body:**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### 2. GET Specific Company
```bash
curl -X GET http://127.0.0.1:5000/api/hubspot/companies/companies/123456789 \
  -H "Content-Type: application/json" \
  -d '{"token": "your_jwt_token"}'
```

**Request Body:**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### 3. CREATE Company
```bash
curl -X POST http://127.0.0.1:5000/api/hubspot/companies/companies \
  -H "Content-Type: application/json" \
  -d '{
    "token": "your_jwt_token",
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

### 4. UPDATE Company
```bash
curl -X PATCH http://127.0.0.1:5000/api/hubspot/companies/companies/123456789 \
  -H "Content-Type: application/json" \
  -d '{
    "token": "your_jwt_token",
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

### 5. DELETE Company
```bash
curl -X DELETE http://127.0.0.1:5000/api/hubspot/companies/companies/123456789 \
  -H "Content-Type: application/json" \
  -d '{
    "token": "your_jwt_token",
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

# GET Companies
response = requests.get(
    'http://127.0.0.1:5000/api/hubspot/companies/companies',
    json={'token': token},
    params={'limit': 5, 'properties': 'name,domain'}
)

# CREATE Company
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
    json=create_data
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

// GET Companies
const companiesResponse = await fetch(
  'http://127.0.0.1:5000/api/hubspot/companies/companies?limit=5&properties=name,domain',
  {
    method: 'GET',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({token})
  }
);

// CREATE Company
const createData = {
  token,
  session_id: 1,
  chat_message_id: 1,
  properties: {
    name: 'New Company',
    domain: 'newcompany.com',
    industry: 'TECHNOLOGY'
  }
};

const createResponse = await fetch(
  'http://127.0.0.1:5000/api/hubspot/companies/companies',
  {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(createData)
  }
);
```

## Key Changes

### Before (Header-based)
```bash
curl -H "Authorization: Bearer your_token" \
     http://127.0.0.1:5000/api/hubspot/companies/companies
```

### After (Body-based)
```bash
curl -X GET http://127.0.0.1:5000/api/hubspot/companies/companies \
  -H "Content-Type: application/json" \
  -d '{"token": "your_token"}'
```

## Benefits

1. **Simpler Integration**: No need to manage Authorization headers
2. **Consistent Format**: All requests use JSON body
3. **Better Logging**: Token is part of request body for better tracking
4. **Easier Testing**: All parameters in one JSON object

## Error Handling

### Missing Token
```json
{
  "error": "Token is required in request body"
}
```

### Invalid Token
```json
{
  "error": "Invalid token: Token has expired"
}
```

### Validation Error
```json
{
  "error": "Validation error",
  "details": {
    "token": ["Missing data for required field."]
  }
}
```
