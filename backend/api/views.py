import json
from wsgiref import headers
from django.http import JsonResponse, HttpResponse
from django.forms.models import model_to_dict
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
        # model to dict , parametr fields - pozwala zwrócić tylko wybrane pola narrow down data from a model instance
        data = model_to_dict(model_data, fields=['id', 'title', 'price'])

    # The Hard Way - HttpResponse
    # return HttpResponse(data) # Content-Type': 'text/html; w kliencie
    # return HttpResponse(data, headers={'content-type': 'application/json'}) # 'content-type': 'application/json' w kliencie ale error w klience print(get_response.json())
    
    # json_data_string = json.dumps(data)  # nie konwertuje wszystkiego na słwonik np pole typu Decimal, trzbea warstwami agneiżdżone dane ręcznie konwertować
    # return HttpResponse(json_data_string, headers={'content-type': 'application/json'}) # 'content-type': 'application/json' 
    # w kliencie  raise RequestsJSONDecodeError(e.msg, e.doc, e.pos) requests.exceptions.JSONDecodeError: Expecting value: line 1 column 1 (char 0)
    #serwer przez pole price
    # raise TypeError(f'Object of type {o.__class__.__name__} '
    # TypeError: Object of type Decimal is not JSON serializable

    #prostrze - JsonResponse
    return JsonResponse(data)