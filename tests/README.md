# API Security Validation Framework

A comprehensive API security testing framework using **pytest**, **Page Object Model (POM)** design pattern, and **HTML reporting**. This framework validates JWT authentication, authorization, rate limiting, schema validation, and token scope management.

## Features

✅ **Authentication Testing**
- User registration and login validation
- Password strength enforcement
- Invalid credentials handling
- Token generation and validation

✅ **Authorization Testing**
- Role-based access control (Admin, User, Guest)
- Scope-based permissions (read, write, delete, admin)
- Privilege escalation prevention
- Protected endpoint access control

✅ **Rate Limiting Testing**
- Registration endpoint (5 requests/minute)
- Login endpoint (10 requests/minute)
- Product operations (10-30 requests/minute)
- Admin operations (5-20 requests/minute)

✅ **Schema Validation Testing**
- Request payload validation
- Response structure verification
- Data type enforcement
- Required field checking

✅ **JWT Token Scope Validation**
- Token structure validation
- Scope enforcement
- Token expiration handling
- Invalid signature detection
- Role-scope consistency

## Architecture

### Page Object Model (POM) Structure

```
tests/
├── conftest.py              # Pytest fixtures and configuration
├── pytest.ini               # Pytest settings
├── pages/                   # POM layer
│   ├── base_api.py         # Base API class with common methods
│   ├── auth_api.py         # Authentication endpoints
│   └── protected_api.py    # Protected endpoints
├── test_authentication.py   # Authentication test cases
├── test_authorization.py    # Authorization test cases
├── test_rate_limiting.py    # Rate limiting test cases
├── test_schema_validation.py # Schema validation test cases
└── test_jwt_scopes.py      # JWT scope validation test cases
```

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login and get JWT token
- `GET /api/me` - Get current user info (protected)

### Products (Protected)
- `GET /api/products` - List all products (read scope)
- `GET /api/products/{id}` - Get single product (read scope)
- `POST /api/products` - Create product (write scope)
- `PUT /api/products/{id}` - Update product (write scope)
- `DELETE /api/products/{id}` - Delete product (delete scope)

### Admin (Protected)
- `GET /api/admin/users` - List all users (admin role)
- `DELETE /api/admin/users/{id}` - Delete user (admin role)
- `POST /api/admin/elevate/{id}` - Elevate user to admin (admin scope)

## User Roles and Scopes

| Role  | Scopes                        |
|-------|-------------------------------|
| Admin | read, write, delete, admin    |
| User  | read, write                   |
| Guest | read                          |

## Setup and Installation

### Prerequisites
- Python 3.8+
- MongoDB running on localhost:27017
- FastAPI backend running

### Install Dependencies

```bash
cd /app
pip install -r backend/requirements.txt
```

### Start Backend Server

The backend should be running on `http://localhost:8001`

```bash
sudo supervisorctl restart backend
```

## Running Tests

### Run All Tests

```bash
cd /app
pytest tests/ -v
```

### Run Specific Test Categories

```bash
# Authentication tests only
pytest tests/ -v -m auth

# Authorization tests only
pytest tests/ -v -m authz

# Rate limiting tests only
pytest tests/ -v -m rate_limit

# Schema validation tests only
pytest tests/ -v -m schema

# JWT scope tests only
pytest tests/ -v -m scope
```

### Generate HTML Report

```bash
cd /app
pytest tests/ --html=test_reports/report.html --self-contained-html
```

The HTML report will be generated at `test_reports/report.html`

### Run with Custom Base URL

```bash
export API_BASE_URL=http://localhost:8001/api
pytest tests/ -v
```

## Test Fixtures

The framework provides reusable fixtures in `conftest.py`:

- `api_base_url` - Base API URL
- `test_user_credentials` - Test user credentials
- `admin_user_credentials` - Admin user credentials
- `guest_user_credentials` - Guest user credentials
- `registered_user` - Registered user with token
- `registered_admin` - Registered admin with token
- `registered_guest` - Registered guest with token
- `test_product_data` - Sample product data

## Test Examples

### Authentication Test

```python
def test_successful_login(self, api_base_url, registered_user):
    auth_api = AuthAPI(api_base_url)
    response = auth_api.login_response(
        registered_user["email"],
        registered_user["password"]
    )
    auth_api.assert_status_code(response, 200)
```

### Authorization Test

```python
def test_user_cannot_delete_product(self, api_base_url, registered_user):
    api = ProtectedAPI(api_base_url)
    response = api.delete_product(product_id, registered_user["token"])
    api.assert_status_code(response, 403)
```

### Rate Limiting Test

```python
def test_registration_rate_limit(self, api_base_url):
    auth_api = AuthAPI(api_base_url)
    responses = []
    for i in range(6):
        response = auth_api.register_response(...)
        responses.append(response)
    
    rate_limited = any(r.status_code == 429 for r in responses)
    assert rate_limited
```

## CI/CD Integration

### GitHub Actions Example

```yaml
name: API Security Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: pip install -r backend/requirements.txt
    
    - name: Run tests
      run: pytest tests/ --html=report.html --self-contained-html
    
    - name: Upload test report
      uses: actions/upload-artifact@v2
      with:
        name: test-report
        path: report.html
```

## Security Best Practices Validated

1. ✅ Strong password requirements (minimum 6 characters)
2. ✅ Email validation
3. ✅ JWT token expiration (30 minutes)
4. ✅ Rate limiting on all endpoints
5. ✅ Role-based access control
6. ✅ Scope-based permissions
7. ✅ Input validation and sanitization
8. ✅ Secure password hashing (bcrypt)
9. ✅ Token signature verification
10. ✅ Protection against privilege escalation

## Customization

### Adding New Test Cases

1. Create test file: `test_new_feature.py`
2. Use POM classes from `pages/` directory
3. Add pytest markers in `pytest.ini`
4. Use fixtures from `conftest.py`

### Adding New API Endpoints

1. Add methods to appropriate POM class in `pages/`
2. Create test file for new endpoint
3. Update README with new endpoint documentation

## Troubleshooting

### Backend Not Running
```bash
sudo supervisorctl status backend
sudo supervisorctl restart backend
```

### MongoDB Connection Issues
```bash
sudo systemctl status mongodb
```

### View Test Logs
```bash
pytest tests/ -v -s  # -s shows print statements
```

## License

MIT License

## Support

For issues or questions, please refer to the project documentation or create an issue in the repository.
