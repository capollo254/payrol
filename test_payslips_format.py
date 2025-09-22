import requests
import json

# Base URL for the Django API
base_url = "http://127.0.0.1:8000/api/v1"

# Login first to get a token
login_data = {
    "email": "employee@demo.com",
    "password": "employee123"
}

print("Testing login...")
login_response = requests.post(f"{base_url}/auth/login/", json=login_data)
print(f"Login status: {login_response.status_code}")

if login_response.status_code == 200:
    token = login_response.json().get('token')
    print(f"Token received: {token[:20]}...")
    
    # Set up headers with token
    headers = {
        'Authorization': f'Token {token}',
        'Content-Type': 'application/json'
    }
    
    print("\n--- Testing Payslips Response Format ---")
    
    # Test the payslips endpoint
    print("Testing payslips...")
    payslips_response = requests.get(f"{base_url}/payroll/payslips/", headers=headers)
    print(f"Payslips status: {payslips_response.status_code}")
    if payslips_response.status_code == 200:
        payslips_data = payslips_response.json()
        print(f"Raw response: {json.dumps(payslips_data, indent=2)}")
    else:
        print(f"Error: {payslips_response.text}")

else:
    print(f"Login failed: {login_response.text}")