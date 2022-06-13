from django.http import JsonResponse
import json

def api_home(request, *args, **kwargs):
    # ma emulować echo danych podonie jak "http://httpbin.org/anything"
    # request -> HTTPRequest instancja klasy HTTPRequest z Django nie z biblioteki requests
    print(request.GET) #url query parameters <QueryDict: {'abc': ['123']}>
    print(request.POST) # <QueryDict: {}>

    body = request.body # byte string of JSON data
    print(body) # b'{"query": "Hello World"}'
    data = {}
    try:
        #try catch bo body może nie mieć żadnych JSON data
        data = json.loads(body) #string of JSON data -> Python Dict
    except: 
        pass
    print(data.keys()) # dict_keys(['query'])
    # raise TypeError(f'Object of type {o.__class__.__name__} '
    # TypeError: Object of type HttpHeaders is not JSON serializable
    #headery nie są serializowane, bez DRF trzeba ręcznie obsługiwać formaty - problem bo Django/python nie idelanie współpracuje z JSONem
    data['headers'] = json.dumps(dict(request.headers)) # nowsza wersja zamiast request.META -> request.headers 
    data['content_type'] = request.content_type
    data['parasm'] = dict(request.GET)
    return JsonResponse(dict(data))