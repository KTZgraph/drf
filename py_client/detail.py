import requests

# endpoint = "http://localhost:8000/api/products/1/"
# get_response = requests.get(endpoint, json={'title': 'Abc123', 'price':'abc123', 'content': 'Hello World'}) # HTTP  Request 
# print(get_response.json())

#alt - wszsytkie widoki
# endpoint = "http://localhost:8000/api/products/alt/10/"
# get_response = requests.get(endpoint, json={'title': 'Abc123', 'price':'abc123', 'content': 'Hello World'}) # HTTP  Request 
# print(get_response.json())




# ----- [2:10:29]
endpoint = "http://localhost:8000/api/products/mixin/1/"
get_response = requests.get(endpoint, json={'title': 'Abc123', 'price':'abc123', 'content': 'Hello World'}) # HTTP  Request 
print(get_response.json())


