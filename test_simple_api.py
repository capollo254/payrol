import requests

# Base URL for the Django API
base_url = "http://127.0.0.1:8000/api/v1"

# Test a simple endpoint first
print("Testing welcome endpoint...")
welcome_response = requests.get("http://127.0.0.1:8000/welcome/")
print(f"Welcome status: {welcome_response.status_code}")

# Login as employee to test user authentication
login_data = {
    "email": "employee@demo.com",
    "password": "employee123"
}

print("\nTesting employee login...")
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
    
    print("\n--- Testing Employee Me Endpoint ---")
    
    # Test the "me" endpoint first
    me_response = requests.get(f"{base_url}/employees/employees/me/", headers=headers)
    print(f"My profile status: {me_response.status_code}")
    if me_response.status_code == 200:
        my_data = me_response.json()
        print(f"My profile data: {my_data}")
    else:
        print(f"Error: {me_response.text}")

else:
    print(f"Login failed: {login_response.text}")