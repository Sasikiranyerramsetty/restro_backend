#!/usr/bin/env python3
"""
Simple API test script
Run this after starting the server to test the authentication endpoints
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_signup():
    """Test customer signup"""
    url = f"{BASE_URL}/api/v1/auth/signup"
    data = {
        "name": "Test Customer",
        "email": "test@example.com",
        "phone_number": "+1234567890",
        "password": "pass123"
    }
    
    try:
        response = requests.post(url, json=data)
        print(f"Signup Status: {response.status_code}")
        if response.status_code == 201:
            print("Signup successful!")
            print(f"Response: {response.json()}")
        else:
            print(f"Signup failed: {response.text}")
    except Exception as e:
        print(f"Signup error: {e}")

def test_login():
    """Test user login"""
    url = f"{BASE_URL}/api/v1/auth/login"
    data = {
        "email": "test@example.com",
        "password": "pass123"
    }
    
    try:
        response = requests.post(url, json=data)
        print(f"Login Status: {response.status_code}")
        if response.status_code == 200:
            print("Login successful!")
            result = response.json()
            print(f"Token: {result['access_token'][:50]}...")
            return result['access_token']
        else:
            print(f"Login failed: {response.text}")
    except Exception as e:
        print(f"Login error: {e}")
    return None

def test_protected_endpoint(token):
    """Test protected endpoint"""
    if not token:
        print("No token available for protected endpoint test")
        return
        
    url = f"{BASE_URL}/api/v1/auth/me"
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(url, headers=headers)
        print(f"Protected Endpoint Status: {response.status_code}")
        if response.status_code == 200:
            print("Protected endpoint access successful!")
            print(f"User Info: {response.json()}")
        else:
            print(f"Protected endpoint failed: {response.text}")
    except Exception as e:
        print(f"Protected endpoint error: {e}")

def main():
    print("Testing Restro Backend API")
    print("=" * 40)
    
    # Test signup
    print("\n1. Testing Customer Signup...")
    test_signup()
    
    # Test login
    print("\n2. Testing User Login...")
    token = test_login()
    
    # Test protected endpoint
    print("\n3. Testing Protected Endpoint...")
    test_protected_endpoint(token)
    
    print("\n" + "=" * 40)
    print("API testing completed!")

if __name__ == "__main__":
    main()
