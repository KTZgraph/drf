from rest_framework import generics # są jeszcze widoki na Update, DELETE/Destroy
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404 #alternatywnie form django.http import Http404
from django.http import Http404
from yaml import serialize #do rzucania wyjątków jako zworki na endpoint


from .models import Product
from .serializers import ProductSerializer

class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    #jeśli jestem użytkownikime ammdin to moze chcę pokaząc inne serializer?
    serializer_class = ProductSerializer

    def perform_create(self, serializer): #doatkowa metoda można używć w każdym widoku pdziedziczacym po generics.<>APIView 
        # łatwy sposób na dodanie dodatkowego kontekstu podczas serializowania danych i potem ich zapisywania
        # serializer.save(user=self.request.user) #jak mamy użytkownika który stworyzł obiekt to można go tutaj dopisać 
        # print(serializer)
        print(serializer.validated_data) # OrderedDict([('title', 'This field is done!'), ('price', Decimal('32.99'))])
        title = serializer.validated_data.get('title')
        content = serializer.validated_data.get('content') or None
        if content is None:
            content = title

        serializer.save(content=content)
        # można tutaj 1. dopisać usera serializer.save(user=self.request.user)
        # wysłać sygnał 2. send a Django signal

#można taki lukier słakdniowy
product_list_create_view = ProductListCreateAPIView.as_view()

class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    # można customowe queryset
    # def get_queryset(self):
    #     return super().get_queryset()
    serializer_class = ProductSerializer
    # gdy chce się detail view dla jednego konkretnego obiektu
    #lookup_field = 'pk <- podobnie jak Product.objects.get(pk=123)

class ProductListAPIView(generics.ListAPIView):
    '''
    Not gonna use, bo mogę zmienić 
    ProductCreateAPIView(generics.CreateAPIView) -> ProductListCreateAPIView(generics.ListCreateAPIView)
    '''
    queryset = Product.objects.all()
    # można customowe queryset
    # def get_queryset(self):
    #     return super().get_queryset()
    serializer_class = ProductSerializer
    # gdy chce się detail view dla jednego konkretnego obiektu
    #lookup_field = 'pk <- podobnie jak Product.objects.get(pk=123)


############ 1:45:14 połączenie wszysktich trzech widoków w jeden (fajne gdy nie potrzeba osobnych endpointów)
@api_view(['GET', 'POST']) #CONFUSING :< login is all over the place ale FLEXIBLE <3
def product_alt_view(request, pk=None, *args, **kwargs):
    method = request.method #PUT- update, DESTROY -> delete

    if method == 'GET':
        # et request -> jak w detail view ProductDetailAPIView(generics.RetrieveAPIView)
        #albo list view -> ProductCreateAPIView(generics.CreateAPIView) czy rozxbudowanej wersjiProductListCreateAPIView(generics.ListCreateAPIView)
            
        if pk is not None:
            #detail view
            # obj = Product.objects.filter(pk=pk)
            # if not queryset.exist():
            #     raise Http404

            obj = get_object_or_404(Product, pk=pk) #obiekt albo Http404
            data = ProductSerializer(obj, many=False).data
            return Response(data)

        #list view
        queryset = Product.objects.all() #cześto tylko q jako nazwa zmiennej
        data = ProductSerializer(queryset, many=True).data
        return Response(data)

    if method == 'POST':
        #create an item  -> jak w ProductCreateAPIView(generics.CreateAPIView) czy rozxbudowanej wersjiProductListCreateAPIView(generics.ListCreateAPIView) 
        # KOPIA class  ProductListCreateAPIView metoda perform_create(self, serializer)
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            title = serializer.validated_data.get('title')
            content = serializer.validated_data.get('content') or None
            if content is None:
                content = title
            serializer.save(content=content)
            return Response(serializer.data) 
        return Response({'invalid': "not good data"}, status=400)

         
