import requests

#alt - wszsytkie widoki
endpoint = "http://localhost:8000/api/products/1/update/" #musi być obiket który już istneije bo inaczje nie zadziała

data = {
    'title': 'Hello world my old friend2',
    'price': 2.22
}

get_response = requests.put(endpoint, json=data) # HTTP  Request 
print(get_response.json())

