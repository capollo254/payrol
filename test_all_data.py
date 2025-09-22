import requests
import json

# Base URL for the Django API
base_url = "http://127.0.0.1:8000/api/v1"

# Login as admin to see all data
login_data = {
    "email": "admin@demo.com",
    "password": "admin123"
}

print("Testing admin login...")
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
    
    print("\n--- Checking All Employees ---")
    
    # Test the employees endpoint
    employees_response = requests.get(f"{base_url}/employees/employees/", headers=headers)
    print(f"Employees status: {employees_response.status_code}")
    if employees_response.status_code == 200:
        employees_data = employees_response.json()
        if 'results' in employees_data:
            employees = employees_data['results']
        else:
            employees = employees_data
        
        print(f"Found {len(employees)} employees:")
        for emp in employees:
            print(f"  - {emp.get('full_name', 'No name')}: {emp.get('email', 'No email')} (ID: {emp.get('id')})")
    
    print("\n--- Checking All Payslips ---")
    
    # Test the payslips endpoint
    payslips_response = requests.get(f"{base_url}/payroll/payslips/", headers=headers)
    print(f"Payslips status: {payslips_response.status_code}")
    if payslips_response.status_code == 200:
        payslips_data = payslips_response.json()
        if 'results' in payslips_data:
            payslips = payslips_data['results']
        else:
            payslips = payslips_data
        
        print(f"Found {len(payslips)} payslips:")
        for slip in payslips:
            print(f"  - Employee ID {slip.get('employee')}: {slip.get('payroll_run', {}).get('period_start_date')} to {slip.get('payroll_run', {}).get('period_end_date')}")

else:
    print(f"Login failed: {login_response.text}")