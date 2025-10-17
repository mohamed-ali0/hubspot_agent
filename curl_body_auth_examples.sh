#!/bin/bash

# Body-Based JWT Authentication Examples
# Make sure Flask server is running on http://127.0.0.1:5000

echo "Body-Based JWT Authentication Examples"
echo "======================================"

# Step 1: Get JWT Token
echo "Step 1: Getting JWT token..."
TOKEN_RESPONSE=$(curl -s -X POST http://127.0.0.1:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "test", "password": "test"}')

echo "Login response: $TOKEN_RESPONSE"

# Extract token from response
TOKEN=$(echo $TOKEN_RESPONSE | grep -o '"token":"[^"]*"' | cut -d'"' -f4)
echo "Token: ${TOKEN:0:50}..."

if [ -z "$TOKEN" ]; then
    echo "ERROR: Could not get token. Make sure Flask server is running."
    exit 1
fi

echo ""
echo "Step 2: Testing GET companies with body token..."

# Step 2: GET Companies with body token
curl -X GET http://127.0.0.1:5000/api/hubspot/companies/companies \
  -H "Content-Type: application/json" \
  -d "{\"token\": \"$TOKEN\"}" \
  --get --data-urlencode "limit=3" \
  --data-urlencode "properties=name,domain,industry"

echo ""
echo "Step 3: Testing GET company properties with body token..."

# Step 3: GET Company Properties with body token
curl -X GET http://127.0.0.1:5000/api/hubspot/companies/properties \
  -H "Content-Type: application/json" \
  -d "{\"token\": \"$TOKEN\"}"

echo ""
echo "Step 4: Testing CREATE company with body token..."

# Step 4: CREATE Company with body token
curl -X POST http://127.0.0.1:5000/api/hubspot/companies/companies \
  -H "Content-Type: application/json" \
  -d "{
    \"token\": \"$TOKEN\",
    \"session_id\": 1,
    \"chat_message_id\": 1,
    \"properties\": {
      \"name\": \"Test Company Body Auth\",
      \"domain\": \"testbodyauth.com\",
      \"industry\": \"TECHNOLOGY\",
      \"phone\": \"+1-555-0123\"
    }
  }"

echo ""
echo "Body-based authentication examples completed!"
echo "All requests now use 'token' in the request body instead of Authorization header."
