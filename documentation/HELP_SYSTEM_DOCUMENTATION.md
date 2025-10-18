# HubSpot Logging AI Agent - Help System Documentation

## Overview

The Help System provides comprehensive API documentation with request/response formats and usage tips for all endpoints. The system is designed to be dynamic and easily maintainable through JSON files.

## Features

- **Dynamic Documentation**: All documentation is stored in JSON files, making it easy to update
- **Search Functionality**: Search across all documentation
- **Module Organization**: Documentation is organized by API modules
- **Request/Response Examples**: Complete examples with curl commands
- **Usage Tips**: Practical tips for each endpoint
- **Related Endpoints**: Links to related functionality

## API Endpoints

### 1. Get Help Overview
```
GET /api/help
```
Returns an overview of all available help documentation with module counts.

**Response:**
```json
{
  "title": "HubSpot Logging AI Agent - API Help",
  "description": "Comprehensive API documentation with request/response formats and usage tips",
  "version": "1.0.0",
  "modules": {
    "contacts": {
      "endpoints": ["get_contacts", "create_contact", "update_contact"],
      "count": 3
    },
    "auth": {
      "endpoints": ["login"],
      "count": 1
    }
  },
  "usage": {
    "get_all_endpoints": "/api/help/{module}",
    "get_specific_endpoint": "/api/help/{module}/{endpoint}",
    "search_endpoints": "/api/help/search?q={query}"
  }
}
```

### 2. Get Module Help
```
GET /api/help/{module}
```
Returns help documentation for all endpoints in a specific module.

**Example:** `GET /api/help/contacts`

### 3. Get Specific Endpoint Help
```
GET /api/help/{module}/{endpoint}
```
Returns detailed help documentation for a specific endpoint.

**Example:** `GET /api/help/contacts/create_contact`

### 4. Search Help Documentation
```
GET /api/help/search?q={query}
```
Search across all help documentation.

**Example:** `GET /api/help/search?q=contact`

### 5. Get Available Modules
```
GET /api/help/modules
```
Returns a list of all available modules with endpoint counts.

## JSON File Structure

Each endpoint documentation is stored in a JSON file with the following structure:

```json
{
  "title": "Endpoint Title",
  "description": "Brief description of the endpoint",
  "method": "HTTP Method (GET, POST, PATCH, etc.)",
  "endpoint": "Full endpoint URL",
  "authentication": "Authentication requirements",
  "request": {
    "url": "Endpoint URL",
    "method": "HTTP Method",
    "headers": {
      "Authorization": "Bearer {jwt_token}",
      "Content-Type": "application/json"
    },
    "query_parameters": {
      "param_name": {
        "type": "string",
        "required": true,
        "description": "Parameter description"
      }
    },
    "body": {
      "field_name": {
        "type": "string",
        "required": true,
        "description": "Field description"
      }
    }
  },
  "response": {
    "success": {
      "status_code": 200,
      "body": {
        "example": "response data"
      }
    },
    "error": {
      "status_code": 400,
      "body": {
        "error": "Error message"
      }
    }
  },
  "tips": [
    "Practical tip 1",
    "Practical tip 2"
  ],
  "examples": {
    "example_name": {
      "description": "What this example demonstrates",
      "curl": "curl command example"
    }
  },
  "related_endpoints": [
    "/api/related/endpoint1",
    "/api/related/endpoint2"
  ]
}
```

## File Organization

```
app/api/v1/help/
├── contacts/
│   ├── get_contacts.json
│   ├── create_contact.json
│   └── update_contact.json
├── deals/
│   ├── get_deals.json
│   ├── create_deal.json
│   └── update_deal.json
├── activities/
│   ├── get_meetings.json
│   ├── create_meeting.json
│   └── get_calls.json
├── auth/
│   ├── login.json
│   ├── logout.json
│   └── me.json
└── health/
    ├── health_check.json
    └── test.json
```

## Adding New Documentation

1. **Create JSON File**: Create a new JSON file in the appropriate module directory
2. **Follow Structure**: Use the JSON structure shown above
3. **Include Examples**: Provide practical curl examples
4. **Add Tips**: Include helpful usage tips
5. **Test**: The documentation will be automatically available through the API

## Usage Examples

### Get All Available Modules
```bash
curl -X GET "http://127.0.0.1:5000/api/help/modules"
```

### Get Help for Contacts Module
```bash
curl -X GET "http://127.0.0.1:5000/api/help/contacts"
```

### Get Specific Endpoint Help
```bash
curl -X GET "http://127.0.0.1:5000/api/help/contacts/create_contact"
```

### Search for Documentation
```bash
curl -X GET "http://127.0.0.1:5000/api/help/search?q=create"
```

## Benefits

1. **No Hardcoding**: All documentation is in JSON files
2. **Easy Updates**: Simply update JSON files to change documentation
3. **Searchable**: Built-in search functionality
4. **Comprehensive**: Includes request/response formats, examples, and tips
5. **Organized**: Clear module-based organization
6. **Dynamic**: Automatically discovers new documentation files

## Integration

The help system is fully integrated with the main API and requires no additional setup. It automatically:

- Discovers all JSON files in the help directories
- Provides search functionality across all documentation
- Returns structured responses for easy consumption
- Handles errors gracefully

This system provides a complete, maintainable documentation solution for the HubSpot Logging AI Agent API.
