# HubSpot Logging AI Agent - Test Scripts

This directory contains comprehensive test scripts to verify your HubSpot Logging AI Agent functionality.

## Available Test Scripts

### 1. `simple_test.py` - Quick Test (Recommended)
**Purpose**: Simple, fast test of all endpoints
**Usage**: `python simple_test.py`
**Features**:
- Tests health check
- Tests authentication
- Tests HubSpot endpoints
- Tests other API endpoints
- Displays database contents
- Windows-compatible (no emojis)

### 2. `test_all_endpoints.py` - Comprehensive Test
**Purpose**: Detailed testing with full reporting
**Usage**: `python test_all_endpoints.py`
**Features**:
- Comprehensive endpoint testing
- Detailed test results
- Database inspection
- Test summary with success rates
- Export capabilities

### 3. `quick_test.py` - Interactive Menu
**Purpose**: Interactive testing with menu options
**Usage**: `python quick_test.py`
**Features**:
- Menu-driven interface
- Individual endpoint testing
- Database inspection
- Direct HubSpot API testing

### 4. `inspect_database.py` - Database Inspector
**Purpose**: Detailed database analysis
**Usage**: `python inspect_database.py`
**Features**:
- Database information
- Table inspection
- Schema analysis
- Data export
- Query execution

### 5. `tests/test_hubspot_direct_api.py` - Direct HubSpot API Test
**Purpose**: Test HubSpot API directly (bypasses your wrapper)
**Usage**: `python tests/test_hubspot_direct_api.py`
**Features**:
- Direct HubSpot API testing
- 100% success rate expected
- Tests all HubSpot operations
- Validates your PAT token

## How to Use

### Step 1: Start Your Flask App
```bash
python app/main.py
```

### Step 2: Run Tests
Choose one of the following:

**Quick Test (Recommended for beginners):**
```bash
python simple_test.py
```

**Comprehensive Test:**
```bash
python test_all_endpoints.py
```

**Interactive Testing:**
```bash
python quick_test.py
```

**Database Inspection:**
```bash
python inspect_database.py
```

**Direct HubSpot API Test:**
```bash
python tests/test_hubspot_direct_api.py
```

## Test Results Interpretation

### Health Check
- ✅ **Status: healthy** - Flask app is running correctly
- ✅ **Database: connected** - Database connection is working
- ✅ **HubSpot API: configured** - Your PAT token is loaded

### Authentication
- ✅ **Login successful** - Authentication system is working
- ❌ **Login failed** - Database or authentication issue

### HubSpot Endpoints
- ✅ **Found X items** - HubSpot integration is working
- ❌ **Failed (401)** - Authentication required
- ❌ **Failed (500)** - Server error

### Database Contents
- **No tables found** - Database not initialized
- **X rows** - Database has data
- **Sample data** - Shows actual database contents

## Expected Results

### Working System:
```
[OK] Status: healthy
[OK] Database: connected
[OK] HubSpot API: configured
[OK] Login successful!
[OK] GET Contacts: Found 3 items
[OK] GET Deals: Found 1 items
[OK] GET Notes: Found 4 items
[OK] GET Tasks: Found 3 items
```

### Common Issues:

**1. Flask App Not Running:**
```
[ERROR] Flask app is not running or not accessible
```
**Solution**: Start Flask app with `python app/main.py`

**2. Authentication Failed:**
```
[ERROR] Login failed: 500
```
**Solution**: Database connection issue - check database file

**3. HubSpot Endpoints Failed (401):**
```
[ERROR] GET Contacts: Failed (401)
```
**Solution**: Authentication issue - login failed

**4. No Database Tables:**
```
[INFO] No tables found in database
```
**Solution**: Database not initialized - run database creation

## Troubleshooting

### If Tests Fail:

1. **Check Flask App**: Make sure `python app/main.py` is running
2. **Check Database**: Verify `data/database.db` exists
3. **Check Environment**: Verify `.env` file has correct HubSpot token
4. **Check Direct API**: Run `python tests/test_hubspot_direct_api.py` to verify HubSpot connectivity

### Database Issues:
- Use `python inspect_database.py` to analyze database
- Check if tables exist
- Verify data integrity

### HubSpot Issues:
- Use `python tests/test_hubspot_direct_api.py` to test direct API
- Verify PAT token in `.env` file
- Check HubSpot API connectivity

## Test Script Features

### Database Display
All test scripts show database contents:
- Table names and row counts
- Sample data from each table
- Database file information

### Authentication Testing
- Tests login endpoint
- Validates JWT token generation
- Tests protected endpoints

### HubSpot Integration Testing
- Tests all HubSpot endpoints
- Validates data retrieval
- Checks API connectivity

### Comprehensive Reporting
- Success/failure counts
- Detailed error messages
- Test execution times
- Database verification

## Next Steps

After running tests:

1. **If all tests pass**: Your system is ready for WhatsApp integration
2. **If tests fail**: Use the error messages to identify and fix issues
3. **For database issues**: Use `inspect_database.py` for detailed analysis
4. **For HubSpot issues**: Use direct API tests to verify connectivity

## Support

If you encounter issues:
1. Check the error messages in test output
2. Use `inspect_database.py` for database analysis
3. Verify Flask app is running
4. Check environment variables in `.env` file
