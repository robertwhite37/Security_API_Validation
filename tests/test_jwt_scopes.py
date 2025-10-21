"""JWT token scope validation tests for API security validation"""
import pytest
import jwt
import time
from datetime import datetime, timezone, timedelta
from tests.pages.auth_api import AuthAPI
from tests.pages.protected_api import ProtectedAPI

SECRET_KEY = "your-secret-key-change-in-production-use-strong-key"
ALGORITHM = "HS256"

@pytest.mark.scope
class TestJWTScopeValidation:
    """Test suite for JWT token scope validation"""
    
    def test_user_token_contains_correct_scopes(self, api_base_url, registered_user):
        """Test that user token contains correct scopes"""
        auth_api = AuthAPI(api_base_url)
        response = auth_api.get_current_user(registered_user["token"])
        
        data = response.json()
        assert "scopes" in data
        assert "read" in data["scopes"]
        assert "write" in data["scopes"]
        assert "delete" not in data["scopes"]  # Regular user shouldn't have delete
    
    def test_admin_token_contains_all_scopes(self, api_base_url, registered_admin):
        """Test that admin token contains all scopes"""
        auth_api = AuthAPI(api_base_url)
        response = auth_api.get_current_user(registered_admin["token"])
        
        data = response.json()
        assert "scopes" in data
        assert "read" in data["scopes"]
        assert "write" in data["scopes"]
        assert "delete" in data["scopes"]
        assert "admin" in data["scopes"]
    
    def test_guest_token_has_limited_scopes(self, api_base_url, registered_guest):
        """Test that guest token has limited scopes"""
        auth_api = AuthAPI(api_base_url)
        response = auth_api.get_current_user(registered_guest["token"])
        
        data = response.json()
        assert "scopes" in data
        assert data["scopes"] == ["read"]  # Guest should only have read
    
    def test_read_scope_allows_get_products(self, api_base_url, registered_user):
        """Test that read scope allows GET /products"""
        api = ProtectedAPI(api_base_url)
        response = api.get_products(registered_user["token"])
        
        api.assert_status_code(response, 200, "Read scope should allow GET products")
    
    def test_write_scope_allows_create_product(self, api_base_url, registered_user, test_product_data):
        """Test that write scope allows POST /products"""
        api = ProtectedAPI(api_base_url)
        response = api.create_product(
            registered_user["token"],
            test_product_data["name"],
            test_product_data["description"],
            test_product_data["price"]
        )
        
        api.assert_status_code(response, 201, "Write scope should allow creating products")
    
    def test_delete_scope_required_for_delete(self, api_base_url, registered_user, registered_admin, test_product_data):
        """Test that delete scope is required to delete products"""
        api = ProtectedAPI(api_base_url)
        
        # Admin creates a product
        create_response = api.create_product(
            registered_admin["token"],
            test_product_data["name"],
            test_product_data["description"],
            test_product_data["price"]
        )
        product_id = create_response.json()["id"]
        
        # User without delete scope tries to delete
        response = api.delete_product(product_id, registered_user["token"])
        api.assert_status_code(response, 403, "Delete scope should be required")
        
        # Admin with delete scope can delete
        response = api.delete_product(product_id, registered_admin["token"])
        api.assert_status_code(response, 204, "Admin with delete scope should succeed")
    
    def test_admin_scope_required_for_admin_endpoints(self, api_base_url, registered_user, registered_admin):
        """Test that admin scope is required for admin endpoints"""
        api = ProtectedAPI(api_base_url)
        
        # User without admin scope
        response = api.get_all_users(registered_user["token"])
        api.assert_status_code(response, 403, "Admin scope should be required")
        
        # Admin with admin scope
        response = api.get_all_users(registered_admin["token"])
        api.assert_status_code(response, 200, "Admin scope should grant access")
    
    def test_token_without_scopes_rejected(self, api_base_url):
        """Test that token without scopes is rejected"""
        # Create a token without scopes
        token_data = {
            "sub": "fake-user-id",
            "role": "user",
            "exp": datetime.now(timezone.utc) + timedelta(minutes=30)
        }
        fake_token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
        
        api = ProtectedAPI(api_base_url)
        response = api.get_products(fake_token)
        
        # Should fail because token doesn't have scopes in database user
        api.assert_status_code(response, 401, "Token without valid user should be rejected")
    
    def test_expired_token_rejected(self, api_base_url):
        """Test that expired token is rejected"""
        # Create an expired token
        token_data = {
            "sub": "fake-user-id",
            "role": "user",
            "scopes": ["read", "write"],
            "exp": datetime.now(timezone.utc) - timedelta(minutes=30)  # Expired
        }
        expired_token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
        
        api = ProtectedAPI(api_base_url)
        response = api.get_products(expired_token)
        
        api.assert_status_code(response, 401, "Expired token should be rejected")
    
    def test_token_with_invalid_signature_rejected(self, api_base_url):
        """Test that token with invalid signature is rejected"""
        # Create a token with wrong secret
        token_data = {
            "sub": "fake-user-id",
            "role": "user",
            "scopes": ["read", "write", "admin"],
            "exp": datetime.now(timezone.utc) + timedelta(minutes=30)
        }
        fake_token = jwt.encode(token_data, "wrong-secret-key", algorithm=ALGORITHM)
        
        api = ProtectedAPI(api_base_url)
        response = api.get_products(fake_token)
        
        api.assert_status_code(response, 401, "Token with invalid signature should be rejected")
    
    def test_scope_validation_prevents_privilege_escalation(self, api_base_url, registered_user, registered_guest):
        """Test that users cannot escalate privileges via scope manipulation"""
        api = ProtectedAPI(api_base_url)
        
        # Guest tries to elevate user (should fail - no admin scope)
        response = api.elevate_user(registered_user["user_id"], registered_guest["token"])
        api.assert_status_code(response, 403, "Guest should not be able to elevate users")
    
    def test_role_and_scope_consistency(self, api_base_url, registered_user, registered_admin, registered_guest):
        """Test that roles and scopes are consistent"""
        auth_api = AuthAPI(api_base_url)
        
        # Check user role and scopes
        user_response = auth_api.get_current_user(registered_user["token"])
        user_data = user_response.json()
        assert user_data["role"] == "user"
        assert set(user_data["scopes"]) == {"read", "write"}
        
        # Check admin role and scopes
        admin_response = auth_api.get_current_user(registered_admin["token"])
        admin_data = admin_response.json()
        assert admin_data["role"] == "admin"
        assert set(admin_data["scopes"]) == {"read", "write", "delete", "admin"}
        
        # Check guest role and scopes
        guest_response = auth_api.get_current_user(registered_guest["token"])
        guest_data = guest_response.json()
        assert guest_data["role"] == "guest"
        assert guest_data["scopes"] == ["read"]