import requests
import json

# Base URL for the Django API
base_url = "http://127.0.0.1:8000/api/v1"

print("Testing API endpoints...\n")

# Test login first
login_data = {
    "email": "employee@demo.com", 
    "password": "employee123"
}

print("1. Testing login...")
login_response = requests.post(f"{base_url}/auth/login/", json=login_data)
print(f"   Status: {login_response.status_code}")

if login_response.status_code == 200:
    token = login_response.json().get('token')
    print(f"   Token: {token[:20]}...")
    
    headers = {
        'Authorization': f'Token {token}',
        'Content-Type': 'application/json'
    }
    
    print("\n2. Testing profile endpoint...")
    me_response = requests.get(f"{base_url}/employees/employees/me/", headers=headers)
    print(f"   Status: {me_response.status_code}")
    if me_response.status_code == 200:
        profile_data = me_response.json()
        print(f"   Name: {profile_data.get('full_name', 'N/A')}")
        print(f"   Email: {profile_data.get('email', 'N/A')}")
    else:
        print(f"   Error: {me_response.text}")
    
    print("\n3. Testing payslips endpoint...")
    payslips_response = requests.get(f"{base_url}/payroll/payslips/", headers=headers)
    print(f"   Status: {payslips_response.status_code}")
    if payslips_response.status_code == 200:
        payslips_data = payslips_response.json()
        if 'results' in payslips_data:
            payslips = payslips_data['results']
        else:
            payslips = payslips_data
        print(f"   Found {len(payslips)} payslips")
        for i, payslip in enumerate(payslips[:3]):  # Show first 3
            period = payslip.get('payroll_run', {})
            print(f"   Payslip {i+1}: {period.get('period_start_date')} to {period.get('period_end_date')}")
    else:
        print(f"   Error: {payslips_response.text}")

else:
    print(f"   Login failed: {login_response.text}")

print("\nAPI test completed!")