import requests

endpoint = "http://localhost:8000/api/"
get_response = requests.post(endpoint, json={'title': 'Abc123', 'price':'abc123', 'content': 'Hello World'}) # HTTP  Request 
print(get_response.json())
