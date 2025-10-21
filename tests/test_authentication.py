"""Authentication tests for API security validation"""
import pytest
import time
from tests.pages.auth_api import AuthAPI

@pytest.mark.auth
class TestAuthentication:
    """Test suite for authentication functionality"""
    
    def test_successful_registration(self, api_base_url, test_user_credentials):
        """Test successful user registration"""
        auth_api = AuthAPI(api_base_url)
        response = auth_api.register_response(
            test_user_credentials["email"],
            test_user_credentials["username"],
            test_user_credentials["password"],
            test_user_credentials["role"]
        )
        
        auth_api.assert_status_code(response, 201, "Registration should succeed")
        auth_api.assert_response_contains(response, "message")
        auth_api.assert_response_contains(response, "user_id")
    
    def test_duplicate_email_registration(self, api_base_url, test_user_credentials):
        """Test registration with duplicate email fails"""
        auth_api = AuthAPI(api_base_url)
        
        # First registration
        auth_api.register_response(
            test_user_credentials["email"],
            test_user_credentials["username"],
            test_user_credentials["password"]
        )
        
        # Attempt duplicate registration
        response = auth_api.register_response(
            test_user_credentials["email"],
            "different_username",
            test_user_credentials["password"]
        )
        
        auth_api.assert_status_code(response, 400, "Duplicate email should be rejected")
    
    def test_invalid_password_length(self, api_base_url, test_user_credentials):
        """Test registration with short password fails"""
        auth_api = AuthAPI(api_base_url)
        response = auth_api.register_response(
            test_user_credentials["email"],
            test_user_credentials["username"],
            "123"  # Too short
        )
        
        auth_api.assert_status_code(response, 422, "Short password should be rejected")
    
    def test_invalid_username_length(self, api_base_url):
        """Test registration with short username fails"""
        auth_api = AuthAPI(api_base_url)
        response = auth_api.register_response(
            f"test_{int(time.time())}@example.com",
            "ab",  # Too short
            "password123"
        )
        
        auth_api.assert_status_code(response, 422, "Short username should be rejected")
    
    def test_successful_login(self, api_base_url, registered_user):
        """Test successful login with valid credentials"""
        auth_api = AuthAPI(api_base_url)
        response = auth_api.login_response(
            registered_user["email"],
            registered_user["password"]
        )
        
        auth_api.assert_status_code(response, 200, "Login should succeed")
        assert auth_api.validate_token_response(response), "Token response should have all required fields"
        
        data = response.json()
        assert data["token_type"] == "bearer"
        assert data["role"] == registered_user["role"]
        assert "access_token" in data
    
    def test_login_with_wrong_password(self, api_base_url, registered_user):
        """Test login with incorrect password fails"""
        auth_api = AuthAPI(api_base_url)
        response = auth_api.login_response(
            registered_user["email"],
            "wrongpassword123"
        )
        
        auth_api.assert_status_code(response, 401, "Wrong password should be rejected")
    
    def test_login_with_nonexistent_email(self, api_base_url):
        """Test login with non-existent email fails"""
        auth_api = AuthAPI(api_base_url)
        response = auth_api.login_response(
            "nonexistent@example.com",
            "password123"
        )
        
        auth_api.assert_status_code(response, 401, "Non-existent user should be rejected")
    
    def test_access_protected_endpoint_without_token(self, api_base_url):
        """Test accessing protected endpoint without token fails"""
        auth_api = AuthAPI(api_base_url)
        response = auth_api.get("/me")
        
        auth_api.assert_status_code(response, 403, "Missing token should be rejected")
    
    def test_access_protected_endpoint_with_invalid_token(self, api_base_url):
        """Test accessing protected endpoint with invalid token fails"""
        auth_api = AuthAPI(api_base_url)
        response = auth_api.get("/me", token="invalid.token.here")
        
        auth_api.assert_status_code(response, 401, "Invalid token should be rejected")
    
    def test_access_protected_endpoint_with_valid_token(self, api_base_url, registered_user):
        """Test accessing protected endpoint with valid token succeeds"""
        auth_api = AuthAPI(api_base_url)
        response = auth_api.get_current_user(registered_user["token"])
        
        auth_api.assert_status_code(response, 200, "Valid token should grant access")
        auth_api.assert_response_contains(response, "email", registered_user["email"])
        auth_api.assert_response_contains(response, "role", registered_user["role"])
    
    def test_token_contains_correct_user_info(self, api_base_url, registered_user):
        """Test that token contains correct user information"""
        auth_api = AuthAPI(api_base_url)
        response = auth_api.get_current_user(registered_user["token"])
        
        data = response.json()
        assert data["email"] == registered_user["email"]
        assert data["username"] == registered_user["username"]
        assert data["role"] == registered_user["role"]
        assert "scopes" in data