"""Pytest configuration and fixtures"""
import pytest
import requests
import os
from typing import Dict, Optional
import time

# Base URL for API
BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8001/api")

@pytest.fixture(scope="session")
def api_base_url():
    """Base URL for the API"""
    return BASE_URL

@pytest.fixture(scope="function")
def test_user_credentials():
    """Test user credentials"""
    import random
    unique_id = f"{int(time.time())}{random.randint(1000, 9999)}"
    return {
        "email": f"testuser_{unique_id}@example.com",
        "username": f"testuser_{unique_id}",
        "password": "testpass123",
        "role": "user"
    }

@pytest.fixture(scope="function")
def admin_user_credentials():
    """Admin user credentials"""
    import random
    unique_id = f"{int(time.time())}{random.randint(1000, 9999)}"
    return {
        "email": f"admin_{unique_id}@example.com",
        "username": f"admin_{unique_id}",
        "password": "adminpass123",
        "role": "admin"
    }

@pytest.fixture(scope="function")
def guest_user_credentials():
    """Guest user credentials"""
    import random
    unique_id = f"{int(time.time())}{random.randint(1000, 9999)}"
    return {
        "email": f"guest_{unique_id}@example.com",
        "username": f"guest_{unique_id}",
        "password": "guestpass123",
        "role": "guest"
    }

@pytest.fixture(scope="function")
def registered_user(api_base_url, test_user_credentials):
    """Register a test user and return credentials with token"""
    from tests.pages.auth_api import AuthAPI
    auth_api = AuthAPI(api_base_url)
    
    # Register user
    register_response = auth_api.register(
        test_user_credentials["email"],
        test_user_credentials["username"],
        test_user_credentials["password"],
        test_user_credentials["role"]
    )
    
    # Login to get token
    login_response = auth_api.login(
        test_user_credentials["email"],
        test_user_credentials["password"]
    )
    
    return {
        **test_user_credentials,
        "token": login_response["access_token"],
        "user_id": register_response["user_id"]
    }

@pytest.fixture(scope="function")
def registered_admin(api_base_url, admin_user_credentials):
    """Register an admin user and return credentials with token"""
    from tests.pages.auth_api import AuthAPI
    auth_api = AuthAPI(api_base_url)
    
    # Register admin
    register_response = auth_api.register(
        admin_user_credentials["email"],
        admin_user_credentials["username"],
        admin_user_credentials["password"],
        admin_user_credentials["role"]
    )
    
    # Login to get token
    login_response = auth_api.login(
        admin_user_credentials["email"],
        admin_user_credentials["password"]
    )
    
    return {
        **admin_user_credentials,
        "token": login_response["access_token"],
        "user_id": register_response["user_id"]
    }

@pytest.fixture(scope="function")
def registered_guest(api_base_url, guest_user_credentials):
    """Register a guest user and return credentials with token"""
    from tests.pages.auth_api import AuthAPI
    auth_api = AuthAPI(api_base_url)
    
    # Register guest
    register_response = auth_api.register(
        guest_user_credentials["email"],
        guest_user_credentials["username"],
        guest_user_credentials["password"],
        guest_user_credentials["role"]
    )
    
    # Login to get token
    login_response = auth_api.login(
        guest_user_credentials["email"],
        guest_user_credentials["password"]
    )
    
    return {
        **guest_user_credentials,
        "token": login_response["access_token"],
        "user_id": register_response["user_id"]
    }

@pytest.fixture(scope="function")
def test_product_data():
    """Test product data"""
    return {
        "name": f"Test Product {int(time.time())}",
        "description": "This is a test product",
        "price": 99.99
    }

@pytest.fixture(scope="function")
def cleanup_test_data(api_base_url):
    """Cleanup fixture to remove test data after tests"""
    created_products = []
    
    yield created_products
    
    # Cleanup logic can be added here if needed
    # Note: In a real scenario, you might want to clean up test data