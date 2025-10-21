# API Security Validation Framework

## Project Overview

This is a comprehensive API security validation framework built with **FastAPI**, **pytest**, and the **Page Object Model (POM)** design pattern. It provides complete testing coverage for JWT Bearer token authentication, authorization, rate limiting, schema validation, and token scope management.

## 🏗️ Architecture

### Backend API (FastAPI)
Location: `/app/backend/server.py`

**Security Features:**
- ✅ JWT Bearer token authentication
- ✅ Password hashing with bcrypt
- ✅ Role-based access control (RBAC)
- ✅ Scope-based permissions
- ✅ Rate limiting on all endpoints
- ✅ Input validation with Pydantic
- ✅ MongoDB database integration

**User Roles & Scopes:**
| Role  | Scopes                        | Permissions |
|-------|-------------------------------|-------------|
| Admin | read, write, delete, admin    | Full access to all endpoints |
| User  | read, write                   | Can read and create products |
| Guest | read                          | Read-only access |

**API Endpoints:**

*Authentication:*
- `POST /api/auth/register` - Register new user (5 req/min)
- `POST /api/auth/login` - Login and get JWT token (10 req/min)
- `GET /api/me` - Get current user info (50 req/min)

*Products (Protected):*
- `GET /api/products` - List products (30 req/min, read scope)
- `GET /api/products/{id}` - Get product (30 req/min, read scope)
- `POST /api/products` - Create product (10 req/min, write scope)
- `PUT /api/products/{id}` - Update product (10 req/min, write scope)
- `DELETE /api/products/{id}` - Delete product (5 req/min, delete scope)

*Admin (Protected):*
- `GET /api/admin/users` - List all users (20 req/min, admin role)
- `DELETE /api/admin/users/{id}` - Delete user (5 req/min, admin role)
- `POST /api/admin/elevate/{id}` - Elevate user (5 req/min, admin scope)

### Test Framework (pytest + POM)
Location: `/app/tests/`

**Test Structure:**
```
tests/
├── conftest.py                    # Pytest fixtures & configuration
├── pytest.ini                     # Pytest settings & markers
├── run_tests.sh                   # Test execution script
├── README.md                      # Test framework documentation
├── pages/                         # Page Object Model layer
│   ├── base_api.py               # Base API class with common methods
│   ├── auth_api.py               # Authentication endpoint methods
│   └── protected_api.py          # Protected endpoint methods
├── test_authentication.py         # 11 authentication tests
├── test_authorization.py          # 12 authorization tests
├── test_rate_limiting.py          # 7 rate limiting tests
├── test_schema_validation.py      # 10 schema validation tests
└── test_jwt_scopes.py            # 12 JWT scope validation tests
```

**Total Test Cases: 52**

## 🎯 Test Coverage

### 1. Authentication Tests (11 tests)
- ✅ Successful user registration
- ✅ Duplicate email prevention
- ✅ Password strength validation (min 6 chars)
- ✅ Username length validation (min 3 chars)
- ✅ Successful login with valid credentials
- ✅ Login rejection with wrong password
- ✅ Login rejection for non-existent users
- ✅ Protected endpoint access without token
- ✅ Protected endpoint access with invalid token
- ✅ Protected endpoint access with valid token
- ✅ Token contains correct user information

### 2. Authorization Tests (12 tests)
- ✅ User can read products (read scope)
- ✅ User can create products (write scope)
- ✅ User cannot delete products (missing delete scope)
- ✅ Guest cannot read products (missing read scope)
- ✅ Guest cannot create products (missing write scope)
- ✅ Admin can delete products (has delete scope)
- ✅ User cannot access admin endpoints
- ✅ Admin can access admin endpoints
- ✅ Admin can delete users
- ✅ User cannot delete users
- ✅ Admin can elevate users
- ✅ User cannot elevate users

### 3. Rate Limiting Tests (7 tests)
- ✅ Registration endpoint limit (5/minute)
- ✅ Login endpoint limit (10/minute)
- ✅ Product creation limit (10/minute)
- ✅ Product read limit (30/minute)
- ✅ /me endpoint limit (50/minute)
- ✅ Root endpoint limit (100/minute)
- ✅ Rate limits reset after time window

### 4. Schema Validation Tests (10 tests)
- ✅ Missing required fields rejection
- ✅ Invalid email format rejection
- ✅ Negative price validation
- ✅ Name length validation
- ✅ Product response schema validation
- ✅ Login response schema validation
- ✅ User info response schema validation
- ✅ Extra fields handling

### 5. JWT Token Scope Validation (12 tests)
- ✅ User token contains correct scopes
- ✅ Admin token contains all scopes
- ✅ Guest token has limited scopes
- ✅ Read scope allows GET operations
- ✅ Write scope allows POST operations
- ✅ Delete scope required for DELETE
- ✅ Admin scope required for admin endpoints
- ✅ Token without scopes rejected
- ✅ Expired token rejected
- ✅ Invalid signature rejected
- ✅ Privilege escalation prevention
- ✅ Role-scope consistency validation

## 🚀 Quick Start

### 1. Install Dependencies
```bash
cd /app/backend
pip install -r requirements.txt
```

### 2. Start Backend
```bash
sudo supervisorctl restart backend
```

### 3. Run Tests

**Run all tests:**
```bash
cd /app
pytest tests/ -v --html=test_reports/report.html --self-contained-html
```

**Run specific test categories:**
```bash
pytest tests/ -m auth        # Authentication tests
pytest tests/ -m authz       # Authorization tests
pytest tests/ -m rate_limit  # Rate limiting tests
pytest tests/ -m schema      # Schema validation tests
pytest tests/ -m scope       # JWT scope tests
```

**Run with test script (handles rate limits):**
```bash
cd /app/tests
./run_tests.sh
```

### 4. View HTML Reports
```bash
# View report in browser
cat /app/test_reports/report.html
```

## 📋 Test Execution Examples

### Example 1: Testing Authentication
```bash
pytest tests/test_authentication.py -v
```

**Sample Output:**
```
test_successful_registration PASSED
test_duplicate_email_registration PASSED
test_invalid_password_length PASSED
test_successful_login PASSED
test_access_protected_endpoint_with_valid_token PASSED
```

### Example 2: Testing Authorization
```bash
pytest tests/test_authorization.py::TestAuthorization::test_admin_can_delete_product -v
```

### Example 3: Testing Rate Limiting
```bash
pytest tests/test_rate_limiting.py::TestRateLimiting::test_registration_rate_limit -v
```

## 🔧 Configuration

### Environment Variables
```bash
# Backend .env
MONGO_URL="mongodb://localhost:27017"
DB_NAME="test_database"
SECRET_KEY="your-secret-key-change-in-production-use-strong-key"
CORS_ORIGINS="*"
```

### Pytest Configuration
```ini
# pytest.ini
[pytest]
addopts = -v --html=test_reports/report.html --self-contained-html
testpaths = tests
markers =
    auth: Authentication tests
    authz: Authorization tests
    rate_limit: Rate limiting tests
    schema: Schema validation tests
    scope: JWT scope validation tests
```

## 🏆 Best Practices Implemented

1. **Page Object Model (POM)**: Separates test logic from API interaction
2. **DRY Principle**: Reusable fixtures and base classes
3. **Clear Test Structure**: Descriptive test names and organization
4. **Comprehensive Coverage**: All security aspects tested
5. **HTML Reporting**: Beautiful, detailed test reports
6. **Rate Limit Handling**: Tests respect API rate limits
7. **Data Isolation**: Each test uses unique credentials
8. **Error Handling**: Proper assertion messages
9. **Modular Design**: Easy to extend and maintain
10. **Documentation**: Complete README and inline comments

## 📊 Test Reports

The framework generates HTML reports with:
- Test execution summary
- Pass/fail status for each test
- Detailed error messages
- Execution time
- Environment metadata
- pytest markers

**Report Location:** `/app/test_reports/`

## 🔐 Security Validations

The framework validates:

1. ✅ **Authentication**
   - Password strength (min 6 characters)
   - Email validation
   - Token generation and validation
   - Secure password hashing (bcrypt)

2. ✅ **Authorization**
   - Role-based access control
   - Scope-based permissions
   - Privilege escalation prevention
   - Protected endpoint access

3. ✅ **Rate Limiting**
   - Registration (5/min)
   - Login (10/min)
   - CRUD operations (5-30/min)
   - Admin operations (5-20/min)

4. ✅ **Token Security**
   - JWT signature verification
   - Token expiration (30 minutes)
   - Scope validation
   - Invalid token rejection

5. ✅ **Input Validation**
   - Required field checking
   - Data type enforcement
   - Length validation
   - Format validation

## 🛠️ Extending the Framework

### Adding New Tests
1. Create test file in `/app/tests/`
2. Use existing POM classes from `pages/`
3. Add markers in `pytest.ini`
4. Use fixtures from `conftest.py`

### Adding New API Endpoints
1. Add endpoint to `server.py`
2. Add method to appropriate POM class
3. Create test cases
4. Update documentation

## 📝 Key Files

| File | Purpose |
|------|---------|
| `/app/backend/server.py` | FastAPI application with security features |
| `/app/tests/conftest.py` | Pytest fixtures and configuration |
| `/app/tests/pages/base_api.py` | Base API class with HTTP methods |
| `/app/tests/pages/auth_api.py` | Authentication endpoint methods |
| `/app/tests/pages/protected_api.py` | Protected endpoint methods |
| `/app/tests/test_*.py` | Test case files |
| `/app/tests/pytest.ini` | Pytest configuration |
| `/app/tests/run_tests.sh` | Test execution script |

## 🐛 Troubleshooting

### Backend Not Running
```bash
sudo supervisorctl status backend
sudo supervisorctl restart backend
tail -f /var/log/supervisor/backend.err.log
```

### Rate Limit Issues
```bash
# Wait for rate limits to reset (61 seconds)
sleep 61
# Or drop database to reset
mongosh --eval "db.getSiblingDB('test_database').dropDatabase()"
```

### MongoDB Issues
```bash
sudo systemctl status mongodb
mongosh  # Check connection
```

## 📈 CI/CD Integration

The framework is ready for CI/CD integration:

```yaml
# Example GitHub Actions workflow
- name: Run Security Tests
  run: |
    cd /app
    pytest tests/ --html=report.html --self-contained-html
    
- name: Upload Test Report
  uses: actions/upload-artifact@v2
  with:
    name: security-test-report
    path: report.html
```

## 📚 Documentation

- **Main README**: `/app/tests/README.md`
- **Project Overview**: `/app/PROJECT_OVERVIEW.md` (this file)
- **API Documentation**: Auto-generated at `http://localhost:8001/docs`

## 🎓 Learning Resources

This framework demonstrates:
- RESTful API security best practices
- JWT authentication implementation
- Rate limiting strategies
- Input validation techniques
- Test automation with pytest
- Page Object Model pattern
- Security testing methodologies

## 📞 Support

For issues or questions:
1. Check test output and HTML reports
2. Review backend logs
3. Verify MongoDB connection
4. Check rate limit status

## 🏁 Conclusion

This API security validation framework provides comprehensive testing for modern web application security. It validates authentication, authorization, rate limiting, schema validation, and JWT token management using industry best practices and the Page Object Model pattern.

**Total Test Cases:** 52  
**Test Categories:** 5  
**Security Validations:** 10+  
**HTML Reports:** ✅  
**POM Pattern:** ✅  
**Production-Ready:** ✅
