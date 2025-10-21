"""Schema validation tests for API security validation"""
import pytest
import time
from tests.pages.auth_api import AuthAPI
from tests.pages.protected_api import ProtectedAPI

@pytest.mark.schema
class TestSchemaValidation:
    """Test suite for request/response schema validation"""
    
    def test_register_missing_required_fields(self, api_base_url):
        """Test registration with missing required fields fails"""
        auth_api = AuthAPI(api_base_url)
        
        # Missing password
        response = auth_api.post("/auth/register", data={
            "email": "test@example.com",
            "username": "testuser"
        })
        
        auth_api.assert_status_code(response, 422, "Missing required field should fail")
    
    def test_register_invalid_email_format(self, api_base_url):
        """Test registration with invalid email format fails"""
        auth_api = AuthAPI(api_base_url)
        response = auth_api.register_response(
            "not-an-email",  # Invalid email
            "testuser",
            "password123"
        )
        
        auth_api.assert_status_code(response, 422, "Invalid email format should fail")
    
    def test_login_missing_required_fields(self, api_base_url):
        """Test login with missing required fields fails"""
        auth_api = AuthAPI(api_base_url)
        response = auth_api.post("/auth/login", data={
            "email": "test@example.com"
            # Missing password
        })
        
        auth_api.assert_status_code(response, 422, "Missing required field should fail")
    
    def test_product_creation_missing_fields(self, api_base_url, registered_user):
        """Test product creation with missing required fields fails"""
        api = ProtectedAPI(api_base_url)
        response = api.post("/products", data={
            "name": "Test Product"
            # Missing description and price
        }, token=registered_user["token"])
        
        api.assert_status_code(response, 422, "Missing required fields should fail")
    
    def test_product_creation_invalid_price(self, api_base_url, registered_user):
        """Test product creation with invalid price fails"""
        api = ProtectedAPI(api_base_url)
        response = api.post("/products", data={
            "name": "Test Product",
            "description": "Test Description",
            "price": -10.99  # Negative price
        }, token=registered_user["token"])
        
        api.assert_status_code(response, 422, "Negative price should fail validation")
    
    def test_product_creation_invalid_name_length(self, api_base_url, registered_user):
        """Test product creation with too short name fails"""
        api = ProtectedAPI(api_base_url)
        response = api.post("/products", data={
            "name": "ab",  # Too short
            "description": "Test Description",
            "price": 10.99
        }, token=registered_user["token"])
        
        api.assert_status_code(response, 422, "Short name should fail validation")
    
    def test_product_response_schema(self, api_base_url, registered_user, test_product_data):
        """Test product response has correct schema"""
        api = ProtectedAPI(api_base_url)
        response = api.create_product(
            registered_user["token"],
            test_product_data["name"],
            test_product_data["description"],
            test_product_data["price"]
        )
        
        api.assert_status_code(response, 201)
        
        # Validate response schema
        data = response.json()
        required_fields = ["id", "name", "description", "price", "created_by", "created_at"]
        
        for field in required_fields:
            assert field in data, f"Response should contain {field}"
        
        assert isinstance(data["id"], str)
        assert isinstance(data["name"], str)
        assert isinstance(data["price"], (int, float))
    
    def test_login_response_schema(self, api_base_url, registered_user):
        """Test login response has correct schema"""
        auth_api = AuthAPI(api_base_url)
        response = auth_api.login_response(
            registered_user["email"],
            registered_user["password"]
        )
        
        auth_api.assert_status_code(response, 200)
        
        # Validate response schema
        data = response.json()
        required_fields = ["access_token", "token_type", "expires_in", "user_id", "role", "scopes"]
        
        for field in required_fields:
            assert field in data, f"Response should contain {field}"
        
        assert data["token_type"] == "bearer"
        assert isinstance(data["expires_in"], int)
        assert isinstance(data["scopes"], list)
    
    def test_user_info_response_schema(self, api_base_url, registered_user):
        """Test user info response has correct schema"""
        auth_api = AuthAPI(api_base_url)
        response = auth_api.get_current_user(registered_user["token"])
        
        auth_api.assert_status_code(response, 200)
        
        # Validate response schema
        data = response.json()
        required_fields = ["id", "email", "username", "role", "scopes"]
        
        for field in required_fields:
            assert field in data, f"Response should contain {field}"
        
        assert isinstance(data["scopes"], list)
    
    def test_product_creation_extra_fields_ignored(self, api_base_url, registered_user):
        """Test that extra fields in product creation are handled properly"""
        api = ProtectedAPI(api_base_url)
        response = api.post("/products", data={
            "name": "Test Product",
            "description": "Test Description",
            "price": 99.99,
            "extra_field": "This should be ignored"
        }, token=registered_user["token"])
        
        # Should succeed, extra fields ignored
        auth_api = AuthAPI(api_base_url)
        auth_api.assert_status_code(response, 201, "Extra fields should be ignored")