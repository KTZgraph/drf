import json
from wsgiref import headers
# from django.http import JsonResponse, HttpResponse
from django.forms.models import model_to_dict
from yaml import serialize
from products.models import Product

# 3 wersja
from rest_framework.response import Response
from rest_framework.decorators import api_view

#4 wersja
from products.serializers import ProductSerializer

# 5 wersja
from django.http import JsonResponse

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

# def api_home2(request, *args, **kwargs):
#     model_data = Product.objects.all().order_by('?').first()
#     data = {}
#     if model_data:
#         # model to dict , parametr fields - pozwala zwrócić tylko wybrane pola narrow down data from a model instance
#         data = model_to_dict(model_data, fields=['id', 'title', 'price'])

#     # The Hard Way - HttpResponse
#     # return HttpResponse(data) # Content-Type': 'text/html; w kliencie
#     # return HttpResponse(data, headers={'content-type': 'application/json'}) # 'content-type': 'application/json' w kliencie ale error w klience print(get_response.json())
    
#     # json_data_string = json.dumps(data)  # nie konwertuje wszystkiego na słwonik np pole typu Decimal, trzbea warstwami agneiżdżone dane ręcznie konwertować
#     # return HttpResponse(json_data_string, headers={'content-type': 'application/json'}) # 'content-type': 'application/json' 
#     # w kliencie  raise RequestsJSONDecodeError(e.msg, e.doc, e.pos) requests.exceptions.JSONDecodeError: Expecting value: line 1 column 1 (char 0)
#     #serwer przez pole price
#     # raise TypeError(f'Object of type {o.__class__.__name__} '
#     # TypeError: Object of type Decimal is not JSON serializable

#     #prostrze - JsonResponse
#     return JsonResponse(data)


# @api_view(['GET']) # drf
# def api_home3(request, *args, **kwargs):
#     """
#     DRF API View
#     """
#     #bez DRF sprawdzanie metod
#     # if request.method != "POST":
#     #     return Response({'detail': 'GET not allowed'}, status=405)
#     model_data = Product.objects.all().order_by('?').first()
#     data = {}
#     if model_data:
#         data = model_to_dict(model_data, fields=['id', 'title', 'price', 'sale_price']) #sale_price niewidoczne w kliencie


#     return Response(data) #drf

# @api_view(['GET']) # drf
# def api_home4(request, *args, **kwargs):
#     """
#     DRF API View
#     """
#     #bez DRF sprawdzanie metod
#     # if request.method != "POST":
#     #     return Response({'detail': 'GET not allowed'}, status=405)
#     instance = Product.objects.all().order_by('?').first()
#     data = {}
#     if instance:
#         # data = model_to_dict(instance, fields=['id', 'title', 'price', 'sale_price'])
#         # serilizer za nas zrobi model to dict i jeszcze dołoży pola z metod jak 'sale_price' czy swoje dynamiczne pole 'my_dicsount' do JSONa
#         data = ProductSerializer(instance).data #serilizers data in nice and clean way
#     return Response(data) #drf klient wszystkie pola z serializera {"title":"Hello World again","content":"This product is amazing","price":"12.00","sale_price":"9.60","get_discount":"122"}



# ---------------------1:17:26
# bez rest_frameworka  @api_view(['POST']) - błąd Django czytsego
# Forbidden (CSRF cookie not set.): /api/
# [14/Jun/2022 19:51:51] "POST /api/ HTTP/1.1" 403 2870
# @api_view(['POST']) # drf
# def api_home(request, *args, **kwargs):
#     """
#     DRF API View
#     """
#     data = request.data
#     return JsonResponse(data) 

@api_view(['POST'])
def api_home(request, *args, **kwargs):
    """
    DRF API View
    """
    #walidacja danych przy pomocy serializera <3
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True): #można dodatkowy paramater dać
        # jedyny sposób na zapisywanie instancji
        # instance = serializer.save() #tylko gdy rzeczyiwście chcemy zachować dane
        # instance=form.save() # podobnie jak formsy
        # instance=form.save(commit=False) tego w serilizerze nie można zrobić
        print(serializer.data) #NIE zapisuje danuych
        # data = serializer.data
        return Response(serializer.data) 
        # return Response(instance) # TypeError: Object of type Product is not JSON serializable
    return Response({'invalid': "not good data"}, status=400)
    # Bad Request: /api/
    # [14/Jun/2022 20:09:22] "POST /api/ HTTP/1.1" 400 27