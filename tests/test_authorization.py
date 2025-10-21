"""Authorization tests for API security validation"""
import pytest
from tests.pages.protected_api import ProtectedAPI

@pytest.mark.authz
class TestAuthorization:
    """Test suite for authorization and role-based access control"""
    
    def test_user_can_read_products(self, api_base_url, registered_user):
        """Test user with read scope can access products"""
        api = ProtectedAPI(api_base_url)
        response = api.get_products(registered_user["token"])
        
        api.assert_status_code(response, 200, "User should be able to read products")
    
    def test_user_can_create_product(self, api_base_url, registered_user, test_product_data):
        """Test user with write scope can create products"""
        api = ProtectedAPI(api_base_url)
        response = api.create_product(
            registered_user["token"],
            test_product_data["name"],
            test_product_data["description"],
            test_product_data["price"]
        )
        
        api.assert_status_code(response, 201, "User should be able to create products")
        api.assert_response_contains(response, "id")
        api.assert_response_contains(response, "name", test_product_data["name"])
    
    def test_user_cannot_delete_product(self, api_base_url, registered_user, registered_admin, test_product_data):
        """Test regular user without delete scope cannot delete products"""
        api = ProtectedAPI(api_base_url)
        
        # Admin creates a product
        create_response = api.create_product(
            registered_admin["token"],
            test_product_data["name"],
            test_product_data["description"],
            test_product_data["price"]
        )
        product_id = create_response.json()["id"]
        
        # User tries to delete
        response = api.delete_product(product_id, registered_user["token"])
        
        api.assert_status_code(response, 403, "User without delete scope should not delete products")
    
    def test_guest_cannot_read_products(self, api_base_url, registered_guest):
        """Test guest without read scope cannot access products"""
        api = ProtectedAPI(api_base_url)
        response = api.get_products(registered_guest["token"])
        
        api.assert_status_code(response, 403, "Guest without read scope should not access products")
    
    def test_guest_cannot_create_product(self, api_base_url, registered_guest, test_product_data):
        """Test guest without write scope cannot create products"""
        api = ProtectedAPI(api_base_url)
        response = api.create_product(
            registered_guest["token"],
            test_product_data["name"],
            test_product_data["description"],
            test_product_data["price"]
        )
        
        api.assert_status_code(response, 403, "Guest without write scope should not create products")
    
    def test_admin_can_delete_product(self, api_base_url, registered_admin, test_product_data):
        """Test admin with delete scope can delete products"""
        api = ProtectedAPI(api_base_url)
        
        # Create a product
        create_response = api.create_product(
            registered_admin["token"],
            test_product_data["name"],
            test_product_data["description"],
            test_product_data["price"]
        )
        product_id = create_response.json()["id"]
        
        # Delete the product
        response = api.delete_product(product_id, registered_admin["token"])
        
        api.assert_status_code(response, 204, "Admin should be able to delete products")
    
    def test_user_cannot_access_admin_endpoints(self, api_base_url, registered_user):
        """Test regular user cannot access admin-only endpoints"""
        api = ProtectedAPI(api_base_url)
        response = api.get_all_users(registered_user["token"])
        
        api.assert_status_code(response, 403, "Regular user should not access admin endpoints")
    
    def test_admin_can_access_admin_endpoints(self, api_base_url, registered_admin):
        """Test admin can access admin-only endpoints"""
        api = ProtectedAPI(api_base_url)
        response = api.get_all_users(registered_admin["token"])
        
        api.assert_status_code(response, 200, "Admin should access admin endpoints")
    
    def test_admin_can_delete_users(self, api_base_url, registered_admin, registered_user):
        """Test admin can delete users"""
        api = ProtectedAPI(api_base_url)
        response = api.delete_user(registered_user["user_id"], registered_admin["token"])
        
        api.assert_status_code(response, 204, "Admin should be able to delete users")
    
    def test_user_cannot_delete_users(self, api_base_url, registered_user, registered_guest):
        """Test regular user cannot delete users"""
        api = ProtectedAPI(api_base_url)
        response = api.delete_user(registered_guest["user_id"], registered_user["token"])
        
        api.assert_status_code(response, 403, "Regular user should not delete users")
    
    def test_admin_can_elevate_user(self, api_base_url, registered_admin, registered_user):
        """Test admin can elevate user to admin"""
        api = ProtectedAPI(api_base_url)
        response = api.elevate_user(registered_user["user_id"], registered_admin["token"])
        
        api.assert_status_code(response, 200, "Admin should elevate users")
        api.assert_response_contains(response, "message")
    
    def test_user_cannot_elevate_users(self, api_base_url, registered_user, registered_guest):
        """Test regular user cannot elevate users"""
        api = ProtectedAPI(api_base_url)
        response = api.elevate_user(registered_guest["user_id"], registered_user["token"])
        
        api.assert_status_code(response, 403, "Regular user should not elevate users")