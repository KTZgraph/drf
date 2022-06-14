import requests

# endpoint = "http://localhost:8000/api/products/"

# get_response = requests.get(endpoint)
# print(get_response.json())

# 2:08:00
endpoint = 'http://localhost:8000/api/products/mixin/'
get_response = requests.get(endpoint)
print(get_response.json())
