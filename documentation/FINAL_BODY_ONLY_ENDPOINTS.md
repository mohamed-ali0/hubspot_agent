# Final Body-Only Endpoints - NO URL Parameters

## 🎯 **Complete Body-Only API Design**

**ALL inputs now come from request body. NO URL parameters are used anywhere.**

---

## 📋 **1. GET All Companies**

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

---

## 📋 **2. GET Specific Company**

### **Endpoint:** `POST /api/hubspot/companies/companies/get`

#### **Request Body:**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "company_id": "123456789"
}
```

#### **cURL Example:**
```bash
curl -X POST http://127.0.0.1:5000/api/hubspot/companies/companies/get \
  -H "Content-Type: application/json" \
  -d '{
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "company_id": "123456789"
  }'
```

---

## 📋 **3. CREATE Company**

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

## 📋 **4. UPDATE Company**

### **Endpoint:** `POST /api/hubspot/companies/companies/update`

#### **Request Body:**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "company_id": "123456789",
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
curl -X POST http://127.0.0.1:5000/api/hubspot/companies/companies/update \
  -H "Content-Type: application/json" \
  -d '{
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "company_id": "123456789",
    "session_id": 1,
    "chat_message_id": 1,
    "properties": {
      "name": "Updated Company Name",
      "phone": "+1-555-9999"
    }
  }'
```

---

## 📋 **5. REPLACE Company**

### **Endpoint:** `POST /api/hubspot/companies/companies/replace`

#### **Request Body:**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "company_id": "123456789",
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

## 📋 **6. DELETE Company**

### **Endpoint:** `POST /api/hubspot/companies/companies/delete`

#### **Request Body:**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "company_id": "123456789",
  "session_id": 1,
  "chat_message_id": 1
}
```

#### **cURL Example:**
```bash
curl -X POST http://127.0.0.1:5000/api/hubspot/companies/companies/delete \
  -H "Content-Type: application/json" \
  -d '{
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "company_id": "123456789",
    "session_id": 1,
    "chat_message_id": 1
  }'
```

---

## 📋 **7. SEARCH Companies**

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

## 📋 **8. GET Company Properties**

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

## 📋 **9. GET Specific Property Schema**

### **Endpoint:** `POST /api/hubspot/companies/properties/get`

#### **Request Body:**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "property_name": "name"
}
```

#### **cURL Example:**
```bash
curl -X POST http://127.0.0.1:5000/api/hubspot/companies/properties/get \
  -H "Content-Type: application/json" \
  -d '{
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "property_name": "name"
  }'
```

---

## 📋 **10. BATCH CREATE Companies**

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

## 📋 **11. BATCH UPDATE Companies**

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

## 🚀 **Key Benefits of Complete Body-Only Design**

1. **✅ NO URL Parameters**: All inputs come from request body
2. **✅ Consistent Format**: Every endpoint uses JSON body
3. **✅ Better Security**: No sensitive data in URLs
4. **✅ Easier Integration**: One JSON object for all data
5. **✅ Better Logging**: All parameters tracked together
6. **✅ Client-Friendly**: Simpler to implement in any language
7. **✅ No Encoding Issues**: No URL encoding needed
8. **✅ Better Testing**: All data in request body

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

### **CompanyGetByIdSchema**
```json
{
  "token": "string (required)",
  "company_id": "string (required)"
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
  "company_id": "string (required)",
  "session_id": "integer (required)",
  "chat_message_id": "integer (required)",
  "properties": "object (required)"
}
```

### **CompanyDeleteSchema**
```json
{
  "token": "string (required)",
  "company_id": "string (required)",
  "session_id": "integer (optional, default: 0)",
  "chat_message_id": "integer (optional, default: 0)"
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

---

## 🔧 **Valid Industry Values**

Use these valid industry values when creating/updating companies:

- `COMPUTER_SOFTWARE` ✅
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
- `ENTERTAINMENT`
- `SPORTS`
- `TRAVEL_TOURISM`

---

## ✅ **Complete Body-Only Implementation**

**ALL endpoints now use body-only input:**
- ✅ **GET Companies**: `limit`, `properties` in body
- ✅ **GET Specific Company**: `company_id` in body
- ✅ **CREATE Company**: All data in body
- ✅ **UPDATE Company**: `company_id` and data in body
- ✅ **REPLACE Company**: `company_id` and data in body
- ✅ **DELETE Company**: `company_id` in body
- ✅ **SEARCH Companies**: All search parameters in body
- ✅ **GET Properties**: Token in body
- ✅ **GET Specific Property**: `property_name` in body
- ✅ **BATCH Operations**: All data in body

**NO URL parameters are used anywhere!** 🎯
