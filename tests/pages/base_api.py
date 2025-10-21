"""Base API class for all API page objects"""
import requests
from typing import Dict, Optional, Any
import json

class BaseAPI:
    """Base class for all API page objects following POM pattern"""
    
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = requests.Session()
        self.default_headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
    
    def _get_headers(self, token: Optional[str] = None, extra_headers: Optional[Dict] = None) -> Dict:
        """Build headers with optional authorization token"""
        headers = self.default_headers.copy()
        
        if token:
            headers["Authorization"] = f"Bearer {token}"
        
        if extra_headers:
            headers.update(extra_headers)
        
        return headers
    
    def get(self, endpoint: str, token: Optional[str] = None, params: Optional[Dict] = None, headers: Optional[Dict] = None) -> requests.Response:
        """Make GET request"""
        url = f"{self.base_url}{endpoint}"
        request_headers = self._get_headers(token, headers)
        response = self.session.get(url, headers=request_headers, params=params)
        return response
    
    def post(self, endpoint: str, data: Optional[Dict] = None, token: Optional[str] = None, headers: Optional[Dict] = None) -> requests.Response:
        """Make POST request"""
        url = f"{self.base_url}{endpoint}"
        request_headers = self._get_headers(token, headers)
        response = self.session.post(url, json=data, headers=request_headers)
        return response
    
    def put(self, endpoint: str, data: Optional[Dict] = None, token: Optional[str] = None, headers: Optional[Dict] = None) -> requests.Response:
        """Make PUT request"""
        url = f"{self.base_url}{endpoint}"
        request_headers = self._get_headers(token, headers)
        response = self.session.put(url, json=data, headers=request_headers)
        return response
    
    def delete(self, endpoint: str, token: Optional[str] = None, headers: Optional[Dict] = None) -> requests.Response:
        """Make DELETE request"""
        url = f"{self.base_url}{endpoint}"
        request_headers = self._get_headers(token, headers)
        response = self.session.delete(url, headers=request_headers)
        return response
    
    def patch(self, endpoint: str, data: Optional[Dict] = None, token: Optional[str] = None, headers: Optional[Dict] = None) -> requests.Response:
        """Make PATCH request"""
        url = f"{self.base_url}{endpoint}"
        request_headers = self._get_headers(token, headers)
        response = self.session.patch(url, json=data, headers=request_headers)
        return response
    
    def assert_status_code(self, response: requests.Response, expected_status: int, message: Optional[str] = None):
        """Assert response status code"""
        if message:
            assert response.status_code == expected_status, f"{message}. Got {response.status_code}, expected {expected_status}. Response: {response.text}"
        else:
            assert response.status_code == expected_status, f"Expected {expected_status}, got {response.status_code}. Response: {response.text}"
    
    def assert_response_contains(self, response: requests.Response, key: str, value: Any = None):
        """Assert response JSON contains key and optionally a specific value"""
        json_data = response.json()
        assert key in json_data, f"Key '{key}' not found in response: {json_data}"
        
        if value is not None:
            assert json_data[key] == value, f"Expected {key}={value}, got {json_data[key]}"
    
    def assert_response_schema(self, response: requests.Response, schema: Dict):
        """Assert response JSON matches expected schema"""
        json_data = response.json()
        
        for key, expected_type in schema.items():
            assert key in json_data, f"Key '{key}' not found in response"
            assert isinstance(json_data[key], expected_type), f"Key '{key}' expected type {expected_type}, got {type(json_data[key])}"