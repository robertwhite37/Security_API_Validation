<div align="center">
  <a href="https://robertwhite.vercel.app/" target="_blank">
    <img src="https://raw.githubusercontent.com/robertwhite37/robertwhite37/main/3.png" alt="Robert White Logo" width="300">
  </a>
</div>

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
