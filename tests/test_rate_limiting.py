"""Rate limiting tests for API security validation"""
import pytest
import time
from tests.pages.auth_api import AuthAPI
from tests.pages.protected_api import ProtectedAPI

@pytest.mark.rate_limit
class TestRateLimiting:
    """Test suite for rate limiting functionality"""
    
    def test_registration_rate_limit(self, api_base_url):
        """Test registration endpoint rate limiting (5/minute)"""
        auth_api = AuthAPI(api_base_url)
        
        # Make 6 requests rapidly
        responses = []
        for i in range(6):
            response = auth_api.register_response(
                f"ratelimit_test_{i}_{int(time.time())}@example.com",
                f"ratelimit_user_{i}_{int(time.time())}",
                "password123"
            )
            responses.append(response)
        
        # Last request should be rate limited
        rate_limited = any(r.status_code == 429 for r in responses)
        assert rate_limited, "Rate limiting should be enforced on registration"
    
    def test_login_rate_limit(self, api_base_url, registered_user):
        """Test login endpoint rate limiting (10/minute)"""
        auth_api = AuthAPI(api_base_url)
        
        # Make 11 login attempts rapidly
        responses = []
        for i in range(11):
            response = auth_api.login_response(
                registered_user["email"],
                "wrongpassword"  # Use wrong password to avoid lockout
            )
            responses.append(response)
        
        # Last request should be rate limited
        rate_limited = any(r.status_code == 429 for r in responses)
        assert rate_limited, "Rate limiting should be enforced on login"
    
    def test_product_creation_rate_limit(self, api_base_url, registered_user, test_product_data):
        """Test product creation rate limiting (10/minute)"""
        api = ProtectedAPI(api_base_url)
        
        # Make 11 product creation requests rapidly
        responses = []
        for i in range(11):
            response = api.create_product(
                registered_user["token"],
                f"{test_product_data['name']}_{i}",
                test_product_data["description"],
                test_product_data["price"]
            )
            responses.append(response)
        
        # Last request should be rate limited
        rate_limited = any(r.status_code == 429 for r in responses)
        assert rate_limited, "Rate limiting should be enforced on product creation"
    
    def test_products_read_rate_limit(self, api_base_url, registered_user):
        """Test products read endpoint rate limiting (30/minute)"""
        api = ProtectedAPI(api_base_url)
        
        # Make 31 requests rapidly
        responses = []
        for i in range(31):
            response = api.get_products(registered_user["token"])
            responses.append(response)
        
        # Last request should be rate limited
        rate_limited = any(r.status_code == 429 for r in responses)
        assert rate_limited, "Rate limiting should be enforced on products read"
    
    def test_me_endpoint_rate_limit(self, api_base_url, registered_user):
        """Test /me endpoint rate limiting (50/minute)"""
        auth_api = AuthAPI(api_base_url)
        
        # Make 51 requests rapidly
        responses = []
        for i in range(51):
            response = auth_api.get_current_user(registered_user["token"])
            responses.append(response)
        
        # Last request should be rate limited
        rate_limited = any(r.status_code == 429 for r in responses)
        assert rate_limited, "Rate limiting should be enforced on /me endpoint"
    
    def test_root_endpoint_rate_limit(self, api_base_url):
        """Test root endpoint rate limiting (100/minute)"""
        api = ProtectedAPI(api_base_url)
        
        # Make 101 requests rapidly
        responses = []
        for i in range(101):
            response = api.root()
            responses.append(response)
        
        # Last request should be rate limited
        rate_limited = any(r.status_code == 429 for r in responses)
        assert rate_limited, "Rate limiting should be enforced on root endpoint"
    
    def test_rate_limit_resets_after_time(self, api_base_url):
        """Test that rate limits reset after the time window"""
        auth_api = AuthAPI(api_base_url)
        
        # Make requests up to limit
        for i in range(5):
            auth_api.register_response(
                f"reset_test_{i}_{int(time.time())}@example.com",
                f"reset_user_{i}",
                "password123"
            )
        
        # Wait for rate limit window to reset (61 seconds)
        time.sleep(61)
        
        # This should succeed
        response = auth_api.register_response(
            f"reset_test_after_wait_{int(time.time())}@example.com",
            f"reset_user_after_wait",
            "password123"
        )
        
        auth_api.assert_status_code(response, 201, "Rate limit should reset after time window")