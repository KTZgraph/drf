from rest_framework import generics
from rest_framework import mixins
from rest_framework import permissions # [2:17:25]
from rest_framework import authentication # [2:20:06]
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404 

from .models import Product
from .serializers import ProductSerializer


class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductListAPIView(generics.ListAPIView):
    '''
    Not gonna use, bo mogę zmienić 
    ProductCreateAPIView(generics.CreateAPIView) -> ProductListCreateAPIView(generics.ListCreateAPIView)
    '''
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    def post(self, request, pk=None, *args, **kwargs):
        return self.list(request, *args, **kwargs)


@api_view(['GET', 'POST'])
def product_alt_view(request, pk=None, *args, **kwargs):
    method = request.method 

    if method == 'GET':
        if pk is not None:
            obj = get_object_or_404(Product, pk=pk) 
            data = ProductSerializer(obj, many=False).data
            return Response(data)

        queryset = Product.objects.all()
        data = ProductSerializer(queryset, many=True).data
        return Response(data)

    if method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            title = serializer.validated_data.get('title')
            content = serializer.validated_data.get('content') or None
            if content is None:
                content = title
            serializer.save(content=content)
            return Response(serializer.data) 
        return Response({'invalid': "not good data"}, status=400)



class ProductUpdateAPIView(generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'

    def perform_update(self, serializer):
        instance = serializer.save()
        if not instance.content:
            instance.content = instance.title
            ##


class ProductDestroyAPIView(generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'

    def perform_destroy(self, instance):

        super().perform_destroy(instance) # super() - instancja klasy bazowej


class ProductMixinView( 
    mixins.CreateModelMixin, 
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin, 
    generics.GenericAPIView
    ):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk') 
        if pk is not None:
            return self.retrieve(request, *args, **kwargs ) 
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs) 

    def perform_create(self, serializer):
        print(serializer.validated_data) 
        title = serializer.validated_data.get('title')
        content = serializer.validated_data.get('content') or None
        if content is None:
            content = 'tihs is a signle view doing cool stuff'

        instance = serializer.save(content=content)


# --------------- [2:17:16]
class ProductListCreateAPIView(generics.ListCreateAPIView):
    '''http://localhost:8000/api/products/
    https://www.django-rest-framework.org/api-guide/permissions/
    '''
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # https://www.django-rest-framework.org/api-guide/permissions/#isauthenticated
    # permission_classes = [permissions.IsAuthenticated] #list ani create NIE zadziała
    # https://www.django-rest-framework.org/api-guide/permissions/#isauthenticatedorreadonly
    # permission_classes, authentication_classes ob są już w klasie bazowej w generics.GenericAPIView
    permission_classes = [permissions.IsAuthenticatedOrReadOnly] #create NIE zadziala. list zadziała
    # authentication.SessionAuthentication dajne dla standardowych endpointów dl aużytkownika który loguje się w przeglądarce
    # ale słabe dla 3rd services czy klienta JavaScript
    authentication_classes = [authentication.SessionAuthentication] #jak się admin zaloguje w przeglądarce to widzi wszystko i moze dodawać nowe dane

    def perform_create(self, serializer):
        print(serializer.validated_data)
        title = serializer.validated_data.get('title')
        content = serializer.validated_data.get('content') or None
        if content is None:
            content = title

        instance = serializer.save(content=content)

product_list_create_view = ProductListCreateAPIView.as_view()