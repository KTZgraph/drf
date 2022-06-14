import requests

endpoint = "http://localhost:8000/api/products/alt/435433543545"
get_response = requests.get(endpoint, json={'title': 'Abc123', 'price':'abc123', 'content': 'Hello World'}) # HTTP  Request 
print(get_response.json())
# {'detail': 'Not found.'}
