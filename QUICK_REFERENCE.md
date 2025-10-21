# API Security Validation Framework - Quick Reference

## 📌 Quick Commands

### Run All Tests
```bash
cd /app && pytest tests/ -v
```

### Run Specific Test Categories
```bash
pytest tests/ -m auth              # Authentication tests
pytest tests/ -m authz             # Authorization tests  
pytest tests/ -m rate_limit        # Rate limiting tests
pytest tests/ -m schema            # Schema validation tests
pytest tests/ -m scope             # JWT scope tests
```

### Generate HTML Report
```bash
pytest tests/ --html=test_reports/report.html --self-contained-html
```

### Run Specific Test File
```bash
pytest tests/test_authentication.py -v
pytest tests/test_authorization.py -v
pytest tests/test_rate_limiting.py -v
pytest tests/test_schema_validation.py -v
pytest tests/test_jwt_scopes.py -v
```

### Run Single Test
```bash
pytest tests/test_authentication.py::TestAuthentication::test_successful_login -v
```

### Clean Database Before Tests
```bash
mongosh --eval "db.getSiblingDB('test_database').dropDatabase()"
```

## 🔑 Test User Credentials

Tests automatically create unique users. Manual testing:

```bash
# Register User
curl -X POST http://localhost:8001/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@test.com",
    "username": "testuser",
    "password": "password123",
    "role": "user"
  }'

# Login
curl -X POST http://localhost:8001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@test.com",
    "password": "password123"
  }'

# Use Token (replace YOUR_TOKEN)
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:8001/api/me
```

## 📊 Test Statistics

- **Total Tests**: 52
- **Authentication**: 11 tests
- **Authorization**: 12 tests
- **Rate Limiting**: 7 tests
- **Schema Validation**: 10 tests
- **JWT Scopes**: 12 tests

## 🎯 User Roles & Permissions

| Role  | Scopes                     | Can Do |
|-------|---------------------------|--------|
| Admin | read, write, delete, admin | Everything |
| User  | read, write               | Read/Create products |
| Guest | read                      | Read only |

## 🚦 Rate Limits

| Endpoint | Limit |
|----------|-------|
| POST /api/auth/register | 5/min |
| POST /api/auth/login | 10/min |
| GET /api/me | 50/min |
| GET /api/products | 30/min |
| POST /api/products | 10/min |
| DELETE /api/products/{id} | 5/min |
| GET /api/admin/users | 20/min |
| GET /api/ | 100/min |

## 🔧 Backend Commands

```bash
# Restart backend
sudo supervisorctl restart backend

# Check backend status
sudo supervisorctl status backend

# View backend logs
tail -f /var/log/supervisor/backend.err.log
tail -f /var/log/supervisor/backend.out.log

# Check if backend is running
curl http://localhost:8001/api/health
```

## 📁 Important Files

```
/app/backend/server.py          # FastAPI application
/app/backend/.env               # Environment variables
/app/tests/conftest.py          # Pytest fixtures
/app/tests/pytest.ini           # Pytest config
/app/tests/pages/base_api.py    # Base API class
/app/tests/pages/auth_api.py    # Auth endpoints
/app/tests/pages/protected_api.py # Protected endpoints
/app/test_reports/              # Test reports directory
```

## 🐛 Quick Troubleshooting

### Rate Limit Exceeded
```bash
# Wait 61 seconds or drop database
sleep 61
# OR
mongosh --eval "db.getSiblingDB('test_database').dropDatabase()"
```

### Backend Not Responding
```bash
sudo supervisorctl restart backend
curl http://localhost:8001/api/health
```

### Tests Failing
```bash
# Check backend is running
curl http://localhost:8001/api/health

# Clean database
mongosh --eval "db.getSiblingDB('test_database').dropDatabase()"

# Run with verbose output
pytest tests/ -v -s
```

## 📝 Test Examples

### Example: Test Authentication Flow
```python
def test_full_auth_flow(api_base_url):
    auth_api = AuthAPI(api_base_url)
    
    # Register
    response = auth_api.register_response(
        "test@example.com", "testuser", "password123"
    )
    assert response.status_code == 201
    
    # Login
    response = auth_api.login_response(
        "test@example.com", "password123"
    )
    assert response.status_code == 200
    token = response.json()["access_token"]
    
    # Access protected endpoint
    response = auth_api.get_current_user(token)
    assert response.status_code == 200
```

### Example: Test Authorization
```python
def test_scope_authorization(api_base_url, registered_user):
    api = ProtectedAPI(api_base_url)
    
    # User can read
    response = api.get_products(registered_user["token"])
    assert response.status_code == 200
    
    # User can write
    response = api.create_product(
        registered_user["token"], 
        "Product", "Description", 99.99
    )
    assert response.status_code == 201
```

## 🎓 POM Pattern Example

```python
# Base API class (base_api.py)
class BaseAPI:
    def post(self, endpoint, data, token=None):
        headers = self._get_headers(token)
        return requests.post(f"{self.base_url}{endpoint}", 
                           json=data, headers=headers)

# Auth API class (auth_api.py)
class AuthAPI(BaseAPI):
    def login(self, email, password):
        return self.post("/auth/login", 
                        {"email": email, "password": password})

# Test file
def test_login(api_base_url):
    auth_api = AuthAPI(api_base_url)
    response = auth_api.login_response("user@test.com", "pass123")
    assert response.status_code == 200
```

## 🔄 CI/CD Integration

```yaml
# .github/workflows/test.yml
name: Security Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run Tests
        run: |
          cd /app
          pytest tests/ --html=report.html
      - name: Upload Report
        uses: actions/upload-artifact@v2
        with:
          name: test-report
          path: report.html
```

## 📚 Additional Resources

- **Full Documentation**: `/app/tests/README.md`
- **Project Overview**: `/app/PROJECT_OVERVIEW.md`
- **API Docs**: `http://localhost:8001/docs`
- **Test Reports**: `/app/test_reports/`

## 💡 Tips

1. **Clean database before test runs** to avoid conflicts
2. **Wait 61 seconds** between rate limit tests
3. **Use unique credentials** for each test (fixtures handle this)
4. **Check backend logs** if tests fail unexpectedly
5. **Run tests in categories** to avoid rate limiting

## ✅ Verification Checklist

- [ ] Backend is running (`curl http://localhost:8001/api/health`)
- [ ] MongoDB is accessible (`mongosh`)
- [ ] Python environment is activated
- [ ] Dependencies are installed (`pip list`)
- [ ] Database is clean (optional, for fresh start)
- [ ] Rate limits have reset (if needed)

---

**Last Updated**: 2025-10-20
**Framework Version**: 1.0.0
**Python**: 3.11+
**FastAPI**: 0.110.1
**Pytest**: 8.4.2
