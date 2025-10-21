"""Authentication API page object"""
from tests.pages.base_api import BaseAPI
from typing import Dict, Optional

class AuthAPI(BaseAPI):
    """Page object for authentication endpoints"""
    
    def register(self, email: str, username: str, password: str, role: str = "user") -> Dict:
        """Register a new user"""
        data = {
            "email": email,
            "username": username,
            "password": password,
            "role": role
        }
        response = self.post("/auth/register", data=data)
        if response.status_code == 201:
            return response.json()
        raise Exception(f"Registration failed: {response.status_code} - {response.text}")
    
    def login(self, email: str, password: str) -> Dict:
        """Login and get access token"""
        data = {
            "email": email,
            "password": password
        }
        response = self.post("/auth/login", data=data)
        if response.status_code == 200:
            return response.json()
        raise Exception(f"Login failed: {response.status_code} - {response.text}")
    
    def register_response(self, email: str, username: str, password: str, role: str = "user"):
        """Register a new user and return full response"""
        data = {
            "email": email,
            "username": username,
            "password": password,
            "role": role
        }
        return self.post("/auth/register", data=data)
    
    def login_response(self, email: str, password: str):
        """Login and return full response"""
        data = {
            "email": email,
            "password": password
        }
        return self.post("/auth/login", data=data)
    
    def get_current_user(self, token: str):
        """Get current user information"""
        return self.get("/me", token=token)
    
    def validate_token_response(self, response) -> bool:
        """Validate token response structure"""
        if response.status_code != 200:
            return False
        
        data = response.json()
        required_fields = ["access_token", "token_type", "expires_in", "user_id", "role", "scopes"]
        
        return all(field in data for field in required_fields)