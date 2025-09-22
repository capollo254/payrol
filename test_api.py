#!/usr/bin/env python
"""
Quick API test script to verify API endpoints
"""
import requests
import json

BASE_URL = 'http://localhost:8000'

def test_login():
    """Test login with demo credentials"""
    login_url = f"{BASE_URL}/api/v1/auth/login/"
    credentials = {
        "email": "employee@demo.com",
        "password": "demo123"
    }
    
    try:
        response = requests.post(login_url, json=credentials)
        print(f"Login Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Login Success - Token received: {data.get('token', 'No token')[:20]}...")
            return data.get('token')
        else:
            print(f"Login Failed: {response.text}")
            return None
    except Exception as e:
        print(f"Login Error: {e}")
        return None

def test_employees_api(token):
    """Test employees API endpoint"""
    if not token:
        print("No token available for employees test")
        return
        
    headers = {'Authorization': f'Token {token}'}
    url = f"{BASE_URL}/api/v1/employees/employees/"
    
    try:
        response = requests.get(url, headers=headers)
        print(f"\nEmployees API Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Employees API Success - Count: {data.get('count', 0)}")
            if 'results' in data and data['results']:
                print(f"First employee: {data['results'][0].get('full_name', 'No name')}")
        else:
            print(f"Employees API Failed: {response.text[:200]}...")
            
    except Exception as e:
        print(f"Employees API Error: {e}")

def test_profile_api(token):
    """Test profile API endpoint"""
    if not token:
        print("No token available for profile test")
        return
        
    headers = {'Authorization': f'Token {token}'}
    url = f"{BASE_URL}/api/v1/employees/employees/me/"
    
    try:
        response = requests.get(url, headers=headers)
        print(f"\nProfile API Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Profile API Success - Name: {data.get('full_name', 'No name')}")
        else:
            print(f"Profile API Failed: {response.text[:200]}...")
            
    except Exception as e:
        print(f"Profile API Error: {e}")

def test_payslips_api(token):
    """Test payslips API endpoint"""
    if not token:
        print("No token available for payslips test")
        return
        
    headers = {'Authorization': f'Token {token}'}
    url = f"{BASE_URL}/api/v1/payroll/payslips/"
    
    try:
        response = requests.get(url, headers=headers)
        print(f"\nPayslips API Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Payslips API Success - Count: {data.get('count', 0)}")
            if 'results' in data and data['results']:
                print(f"First payslip: {data['results'][0].get('pay_period', 'No period')}")
        else:
            print(f"Payslips API Failed: {response.text[:200]}...")
            
    except Exception as e:
        print(f"Payslips API Error: {e}")

if __name__ == "__main__":
    print("Testing API endpoints...")
    
    # Test login and get token
    token = test_login()
    
    # Test API endpoints
    test_employees_api(token)
    test_profile_api(token)
    test_payslips_api(token)
    
    print("\nAPI test completed!")