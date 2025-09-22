import requests

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
    
    print("\n--- Testing Employee Endpoints ---")
    
    # Test the employees list endpoint
    print("Testing employees list...")
    employees_response = requests.get(f"{base_url}/employees/employees/", headers=headers)
    print(f"Employees list status: {employees_response.status_code}")
    if employees_response.status_code == 200:
        employees_data = employees_response.json()
        print(f"Employees response type: {type(employees_data)}")
        print(f"Employees data: {employees_data}")
        
        # Check if it's a paginated response or a list
        if isinstance(employees_data, dict) and 'results' in employees_data:
            employees_list = employees_data['results']
        elif isinstance(employees_data, list):
            employees_list = employees_data
        else:
            employees_list = []
            
        print(f"Number of employees returned: {len(employees_list)}")
        if employees_list:
            print(f"First employee: {employees_list[0].get('full_name', 'No name')}")
    else:
        print(f"Error: {employees_response.text}")
    
    # Test the "me" endpoint
    print("\nTesting my profile endpoint...")
    me_response = requests.get(f"{base_url}/employees/employees/me/", headers=headers)
    print(f"My profile status: {me_response.status_code}")
    if me_response.status_code == 200:
        my_data = me_response.json()
        print(f"My profile: {my_data.get('full_name', 'No name')}")
        print(f"Employee ID: {my_data.get('employee_id', 'No ID')}")
    else:
        print(f"Error: {me_response.text}")
    
    print("\n--- Testing Payroll Endpoints ---")
    
    # Test the payslips endpoint
    print("Testing payslips...")
    payslips_response = requests.get(f"{base_url}/payroll/payslips/", headers=headers)
    print(f"Payslips status: {payslips_response.status_code}")
    if payslips_response.status_code == 200:
        payslips_data = payslips_response.json()
        print(f"Payslips response type: {type(payslips_data)}")
        
        # Check if it's a paginated response or a list
        if isinstance(payslips_data, dict) and 'results' in payslips_data:
            payslips_list = payslips_data['results']
        elif isinstance(payslips_data, list):
            payslips_list = payslips_data
        else:
            payslips_list = []
            
        print(f"Number of payslips returned: {len(payslips_list)}")
        if payslips_list:
            print(f"Latest payslip period: {payslips_list[0].get('payroll_run', {}).get('period_start_date', 'No date')}")
    else:
        print(f"Error: {payslips_response.text}")

else:
    print(f"Login failed: {login_response.text}")