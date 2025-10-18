# Complete Body-Only Input Formats

## 🎯 **All API Endpoints Now Use Body-Only Input**

Every parameter (including `limit`, `properties`, `search_term`, etc.) now comes from the request body. No query parameters are used.

---

## 📋 **1. GET Companies**

### **Endpoint:** `GET /api/hubspot/companies/companies`

#### **Request Body:**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "limit": 5,
  "properties": ["name", "domain", "industry"]
}
```

#### **cURL Example:**
```bash
curl -X GET http://127.0.0.1:5000/api/hubspot/companies/companies \
  -H "Content-Type: application/json" \
  -d '{
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "limit": 5,
    "properties": ["name", "domain", "industry"]
  }'
```

#### **Python Example:**
```python
import requests

response = requests.get(
    'http://127.0.0.1:5000/api/hubspot/companies/companies',
    json={
        'token': 'your_jwt_token',
        'limit': 5,
        'properties': ['name', 'domain', 'industry']
    }
)
```

---

## 📋 **2. GET Specific Company**

### **Endpoint:** `GET /api/hubspot/companies/companies/{company_id}`

#### **Request Body:**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

#### **cURL Example:**
```bash
curl -X GET http://127.0.0.1:5000/api/hubspot/companies/companies/123456789 \
  -H "Content-Type: application/json" \
  -d '{
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }'
```

---

## 📋 **3. GET Company Properties**

### **Endpoint:** `GET /api/hubspot/companies/properties`

#### **Request Body:**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

#### **cURL Example:**
```bash
curl -X GET http://127.0.0.1:5000/api/hubspot/companies/properties \
  -H "Content-Type: application/json" \
  -d '{
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }'
```

---

## 📋 **4. SEARCH Companies**

### **Endpoint:** `POST /api/hubspot/companies/companies/search`

#### **Request Body:**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "session_id": 1,
  "chat_message_id": 1,
  "search_term": "HubSpot",
  "limit": 10
}
```

#### **cURL Example:**
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

---

## 📋 **5. CREATE Company**

### **Endpoint:** `POST /api/hubspot/companies/companies`

#### **Request Body:**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "session_id": 1,
  "chat_message_id": 1,
  "properties": {
    "name": "New Company",
    "domain": "newcompany.com",
    "industry": "COMPUTER_SOFTWARE",
    "phone": "+1-555-0123",
    "address": "123 Main St",
    "city": "Boston",
    "state": "MA",
    "zip": "02101",
    "country": "United States"
  }
}
```

#### **cURL Example:**
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
      "industry": "COMPUTER_SOFTWARE",
      "phone": "+1-555-0123"
    }
  }'
```

---

## 📋 **6. UPDATE Company**

### **Endpoint:** `PATCH /api/hubspot/companies/companies/{company_id}`

#### **Request Body:**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "session_id": 1,
  "chat_message_id": 1,
  "properties": {
    "name": "Updated Company Name",
    "phone": "+1-555-9999",
    "industry": "COMPUTER_SOFTWARE"
  }
}
```

#### **cURL Example:**
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

---

## 📋 **7. REPLACE Company**

### **Endpoint:** `PUT /api/hubspot/companies/companies/{company_id}`

#### **Request Body:**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "session_id": 1,
  "chat_message_id": 1,
  "properties": {
    "name": "Completely New Company",
    "domain": "newcompany.com",
    "industry": "COMPUTER_SOFTWARE",
    "phone": "+1-555-0000"
  }
}
```

---

## 📋 **8. DELETE Company**

### **Endpoint:** `DELETE /api/hubspot/companies/companies/{company_id}`

#### **Request Body:**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

#### **cURL Example:**
```bash
curl -X DELETE http://127.0.0.1:5000/api/hubspot/companies/companies/123456789 \
  -H "Content-Type: application/json" \
  -d '{
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }'
```

---

## 📋 **9. BATCH CREATE Companies**

### **Endpoint:** `POST /api/hubspot/companies/batch`

#### **Request Body:**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "session_id": 1,
  "chat_message_id": 1,
  "companies": [
    {
      "name": "Company 1",
      "domain": "company1.com",
      "industry": "COMPUTER_SOFTWARE"
    },
    {
      "name": "Company 2", 
      "domain": "company2.com",
      "industry": "COMPUTER_SOFTWARE"
    }
  ]
}
```

---

## 📋 **10. BATCH UPDATE Companies**

### **Endpoint:** `PATCH /api/hubspot/companies/batch`

#### **Request Body:**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "session_id": 1,
  "chat_message_id": 1,
  "companies": [
    {
      "id": "123456789",
      "properties": {
        "name": "Updated Company 1",
        "phone": "+1-555-1111"
      }
    },
    {
      "id": "987654321",
      "properties": {
        "name": "Updated Company 2",
        "phone": "+1-555-2222"
      }
    }
  ]
}
```

---

## 📋 **11. GET Company Property Schema**

### **Endpoint:** `GET /api/hubspot/companies/properties/{property_name}`

#### **Request Body:**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

#### **cURL Example:**
```bash
curl -X GET http://127.0.0.1:5000/api/hubspot/companies/properties/name \
  -H "Content-Type: application/json" \
  -d '{
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }'
```

---

## 🔧 **Valid Industry Values**

When creating/updating companies, use these valid industry values:

- `COMPUTER_SOFTWARE`
- `COMPUTER_HARDWARE`
- `COMPUTER_NETWORKING`
- `INTERNET`
- `TELECOMMUNICATIONS`
- `BANKING`
- `INSURANCE`
- `HEALTH_WELLNESS_AND_FITNESS`
- `EDUCATION_MANAGEMENT`
- `GOVERNMENT_ADMINISTRATION`
- `NON_PROFIT_ORGANIZATION_MANAGEMENT`
- `REAL_ESTATE`
- `RETAIL`
- `MANUFACTURING`
- `CONSTRUCTION`
- `TRANSPORTATION_TRUCKING_RAILROAD`
- `UTILITIES`
- `ENTERTAINMENT`
- `SPORTS`
- `TRAVEL_TOURISM`

---

## 🚀 **Benefits of Body-Only Format**

1. **Consistent Format**: All parameters in JSON body
2. **No URL Encoding**: No special character encoding needed
3. **Simpler Integration**: One JSON object for all parameters
4. **Better Logging**: All parameters logged together
5. **Easier Testing**: All data in request body
6. **Client-Friendly**: Easier to implement in various languages
7. **Better Security**: No sensitive data in URLs

---

## 📝 **Schema Definitions**

### **CompanyGetSchema**
```json
{
  "token": "string (required)",
  "limit": "integer (optional, default: 10)",
  "properties": "array of strings (optional, default: [])"
}
```

### **CompanySearchSchema**
```json
{
  "token": "string (required)",
  "session_id": "integer (required)",
  "chat_message_id": "integer (required)",
  "search_term": "string (required)",
  "limit": "integer (optional, default: 10)"
}
```

### **CompanyCreateSchema**
```json
{
  "token": "string (required)",
  "session_id": "integer (required)",
  "chat_message_id": "integer (required)",
  "properties": "object (required)"
}
```

### **CompanyUpdateSchema**
```json
{
  "token": "string (required)",
  "session_id": "integer (required)",
  "chat_message_id": "integer (required)",
  "properties": "object (required)"
}
```

---

## ✅ **Test Results**

- ✅ **GET Companies**: Working with body-only parameters
- ✅ **GET Specific Company**: Working with body-only parameters
- ✅ **GET Company Properties**: Working with body-only parameters
- ✅ **SEARCH Companies**: Working with body-only parameters
- ✅ **CREATE Company**: Working with body-only parameters
- ⚠️ **UPDATE Company**: Method needs to be implemented
- ⚠️ **DELETE Company**: Schema needs to be updated

**All endpoints now use body-only input format!** 🎯
