import requests
# API Application programming interface
# Phone -> Camera -> App -> API -> CAMERA to nie jest REST API tylko biblioteki
# REST APIs -> Web API nie jedyne api jakie aplikacja webowa może mieć można myslec jak o web-api
# wukorzystuje zapytania HTTP Request


endpoint = "http://httpbin.org/status/200"
endpoint = "http://httpbin.org/"


endpoint = "http://httpbin.org/anything" # zwróci odpwoiedź formatted data that my actual python application could in theory use
# HTTP REQUEST -> HTML z drugiej strony HTTP  Request from non-api request will give you a html 
# REST API HTTP Request -> JSON(xml) a rest api request which is still HTTP will send back usually something called JSON or XML
# On one hand a web api allows your application to work with another application through the web, through the internet - some sort of internet request
# when it comes to an http request you get html - that's made for the browser, that's made for humans to look at
#REAST APIs isn't really made for humans to look at; it's meant for software to communicate with each other over the web

#requests.get pozwala na wysyłanei własnych jsonów przez parametr json=słwonik pythona
# get_response = requests.get(endpoint, json={'query': 'Hello World'})  #emuluje HTTP Request
# print(get_response.text)
#   "headers": {
#     "Accept": "*/*",
#     "Accept-Encoding": "gzip, deflate",
#     "Content-Length": "24",
#     "Content-Type": "application/json",
#     ...
#   "json": {
#     "query": "Hello World"
#   },

# requests.get pozwala na przesłanie surowych danych przez parametr data
# get_response = requests.get(endpoint, data={'query': 'Hello World'})  #emuluje HTTP Request
# print(get_response.text) # print raw text response - source code z podglądu przeglądarki
#   "headers": {
#     "Accept": "*/*",
#     "Accept-Encoding": "gzip, deflate",
#     "Content-Length": "17",
#     "Content-Type": "application/x-www-form-urlencoded",
#     ...
#   "form": {
#     "query": "Hello World"
#   },

# # JAvaScript Object Notation ~ Python Dict (null się nie zgadza ("json": null,))
# #jeśli jest to odpowiedź jsona to możemy wykonać poniższy kod
# print(get_response.json()) #mogę teraz wyprintować jako słownik Pythona ('json': None,)

# We can play around with a bunch of different data types to interact with a REST API
# -> we can send form-data, json data, 
#typically if it's going yo receive  json data you're going to send json data, so what you send you typically receive - zwyczajowo
# REST API klient nie zależy ani od technologi tutaj pythona, ani od backendu 
# idea REST API it can be consumed across all kinds of different clients
#so you can have almos unlimited amount of clients consuming a REST API as long as they can do these HTTP requests

# endpoint = "http://httpbin.org/anything"
# get_response = requests.get(endpoint, json={'query': 'Hello World'}) # HTTP  Request
# print(get_response.text) #print raw response
# print(get_response.status_code)


endpoint = "http://localhost:8000/"
get_response = requests.get(endpoint, json={'query': 'Hello World'}) # HTTP  Request
print(get_response.text) #print raw response
print(get_response.status_code)