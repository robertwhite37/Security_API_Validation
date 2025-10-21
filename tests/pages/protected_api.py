"""Protected API endpoints page object"""
from tests.pages.base_api import BaseAPI
from typing import Dict, Optional, List

class ProtectedAPI(BaseAPI):
    """Page object for protected endpoints"""
    
    # Product endpoints
    def get_products(self, token: str):
        """Get all products (requires read scope)"""
        return self.get("/products", token=token)
    
    def get_product(self, product_id: str, token: str):
        """Get a single product (requires read scope)"""
        return self.get(f"/products/{product_id}", token=token)
    
    def create_product(self, token: str, name: str, description: str, price: float):
        """Create a product (requires write scope)"""
        data = {
            "name": name,
            "description": description,
            "price": price
        }
        return self.post("/products", data=data, token=token)
    
    def update_product(self, product_id: str, token: str, name: str, description: str, price: float):
        """Update a product (requires write scope)"""
        data = {
            "name": name,
            "description": description,
            "price": price
        }
        return self.put(f"/products/{product_id}", data=data, token=token)
    
    def delete_product(self, product_id: str, token: str):
        """Delete a product (requires delete scope)"""
        return self.delete(f"/products/{product_id}", token=token)
    
    # Admin endpoints
    def get_all_users(self, token: str):
        """Get all users (requires admin role)"""
        return self.get("/admin/users", token=token)
    
    def delete_user(self, user_id: str, token: str):
        """Delete a user (requires admin role)"""
        return self.delete(f"/admin/users/{user_id}", token=token)
    
    def elevate_user(self, user_id: str, token: str):
        """Elevate user to admin (requires admin scope)"""
        return self.post(f"/admin/elevate/{user_id}", token=token)
    
    # Health check
    def health_check(self):
        """Health check endpoint (public)"""
        return self.get("/health")
    
    def root(self):
        """Root endpoint (public with rate limit)"""
        return self.get("/")