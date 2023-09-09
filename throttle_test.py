import requests
import time

jwt_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6IkpvaG4ifQ.2cKJIQV5g1-qF35pDpJYI_FdyhU9-3EZUwi9cxHCq-A"
headers = {'Authorization': f'Bearer {jwt_token}'}

# Replace with your actual API endpoint URL
api_url = 'http://localhost:5000/protected'

# specify the number of requests to be made
num_requests = 10

for i in range(num_requests):
    response = requests.get(api_url, headers=headers)
    print(f'Request {i + 1} - Status Code: {response.status_code}')
    print(f'Response Content: {response.text}')
    time.sleep(1)

#{"token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6IkpvaG4ifQ.2cKJIQV5g1-qF35pDpJYI_FdyhU9-3EZUwi9cxHCq-A"}