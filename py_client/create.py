import requests

# endpoint = "http://localhost:8000/api/products/" #fajnie jakby było /create na końcu

# # get_response = requests.post(endpoint, params={}, json={})
# # print(get_response.json())
# # {'title': ['This field is required.']}
# # serwer
# #Bad Request: /api/products/
# # [14/Jun/2022 20:57:31] "POST /api/products/ HTTP/1.1" 400 37

# data = {
#     'title': 'This field is done!',
#     'price': 32.99
# }
# get_response = requests.post(endpoint, json=data)
# print(get_response.json())





# ---- [2:08:49]
endpoint = "http://localhost:8000/api/products/mixin/" #fajnie jakby było /create na końcu

# get_response = requests.post(endpoint, params={}, json={})
# print(get_response.json())
# {'title': ['This field is required.']}
# serwer
#Bad Request: /api/products/
# [14/Jun/2022 20:57:31] "POST /api/products/ HTTP/1.1" 400 37

data = {
    'title': 'This field is done!',
    'price': 32.99
}
get_response = requests.post(endpoint, json=data)
print(get_response.json()) # {'detail': 'Method "POST" not allowed.'}
#serwer
# Method Not Allowed: /api/products/mixin/
# [14/Jun/2022 23:10:35] "POST /api/products/mixin/ HTTP/1.1" 405 41