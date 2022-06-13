from django.http import JsonResponse
import json
from products.models import Product

# def api_home1(request, *args, **kwargs):
#     # ma emulować echo danych podonie jak "http://httpbin.org/anything"
#     # request -> HTTPRequest instancja klasy HTTPRequest z Django nie z biblioteki requests
#     print(request.GET) #url query parameters <QueryDict: {'abc': ['123']}>
#     print(request.POST) # <QueryDict: {}>

#     body = request.body # byte string of JSON data
#     print(body) # b'{"query": "Hello World"}'
#     data = {}
#     try:
#         #try catch bo body może nie mieć żadnych JSON data
#         data = json.loads(body) #string of JSON data -> Python Dict
#     except: 
#         pass
#     print(data.keys()) # dict_keys(['query'])
#     # raise TypeError(f'Object of type {o.__class__.__name__} '
#     # TypeError: Object of type HttpHeaders is not JSON serializable
#     #headery nie są serializowane, bez DRF trzeba ręcznie obsługiwać formaty - problem bo Django/python nie idelanie współpracuje z JSONem
#     data['headers'] = json.dumps(dict(request.headers)) # nowsza wersja zamiast request.META -> request.headers 
#     data['content_type'] = request.content_type
#     data['parasm'] = dict(request.GET)
#     return JsonResponse(dict(data))

def api_home(request, *args, **kwargs):
    model_data = Product.objects.all().order_by('?').first()
    data = {}
    if model_data:
        data['id'] = model_data.id
        data['title'] = model_data.title
        data['content'] = model_data.content
        data['price'] = model_data.price
        #serialization
        # model instance (model_data)
        # turn to a Python dictionary 
        #return JSON to my client
    return JsonResponse(data)