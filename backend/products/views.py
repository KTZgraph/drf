from rest_framework import generics # są jeszcze widoki na Update, DELETE/Destroy
from rest_framework import mixins # do klas bazujących na generics.GenericAPIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404 #alternatywnie form django.http import Http404
from django.http import Http404
from yaml import serialize #do rzucania wyjątków jako zworki na endpoint


from .models import Product
from .serializers import ProductSerializer

#widac dziedziczenie po mixinach
# class ListCreateAPIView(mixins.ListModelMixin,
#                         mixins.CreateModelMixin,
#                         GenericAPIView):

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

        instance = serializer.save(content=content)
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
    
    def post(self, request, pk=None, *args, **kwargs): # DZIEDIZCZENIE po mixins.ListModelMixin
        #można zaipmlementować tę mmetodę bo generics.ListAPIView dziedziczy z mixins.ListModelMixin
        return self.list(request, *args, **kwargs) # metoda list pochodiz bezpośrednio z mixins.ListModelMixin,


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


# --------- [1:56:05]
# podobne do ProductDetailAPIView z tym że mogą zaierac dodatkowe dane i używać innych HTTP methods
class ProductUpdateAPIView(generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'

    def perform_update(self, serializer):
        instance = serializer.save() # identyko jak instance ProductListCreateAPIView.perform_create
        #można robić dodatkowe rzeczy instance jak trzeba
        if not instance.content:
            instance.content = instance.title
            ##


class ProductDestroyAPIView(generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'

    def perform_destroy(self, instance):
        # https://www.django-rest-framework.org/api-guide/generic-views/#destroyapiview
        #instance można coś zrobić
        super().perform_destroy(instance) # super() - instancja klasy bazowej

# ------------------ [2:04:19]
#te mixiny to ropakowywanie / jawen użycie klas po który dizedzicza klasy  generics. CreateAPIView
# https://www.django-rest-framework.org/api-guide/generic-views/#createapiview
# class CreateAPIView(mixins.CreateModelMixin, generics.GenericAPIView):
#     pass

#ta klasa która ma w sobie wiel emixinów daje sporo FLEXIBILITY and makes things a little more convoluted
#raczej nie powinno sie isć w tę stronę jak nie potrzeba FLEXIBILITY ale daje też sporo extra możliwości
class ProductMixinView( #te mixiny są trochę convoluted i teraz mam widok któy robi dwie rzeczy - listuje wszystkie i/lub zwraca pojedyczny obiekt
    mixins.CreateModelMixin, #POST Create self.create
    mixins.ListModelMixin, #mtoda self.list GET list
    mixins.RetrieveModelMixin, #detail view potrzebuje pola lookup_field = 'pk' GET kontrketynu obiekt self.retrieve
    generics.GenericAPIView
    ):
    # https://www.django-rest-framework.org/api-guide/generic-views/#genericapiview
    

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk' # pole ważne tylko dla metod które z tego pola korzystają mixins.ListModelMixin, czyli metoda self.list ma to pole gdzieś

    def get(self, request, *args, **kwargs):
        # cos abrdzo podobnego w działaniu do generics.ListAPIView chcę tu napisać
        # https://www.django-rest-framework.org/api-guide/generic-views/#listmodelmixin
        # metoda self.list nie patrzy na pole lookup_field = 'pk' 
        print(args, kwargs) # () {'pk': 1}
        pk = kwargs.get('pk') #wtedy nie trzeba w argumentach ustawiać pk = None def get(self, request, pk = None, *args, **kwargs)
        if pk is not None:
            #self.retrieve sama sobie wyciągnie pk z **kwargs  dzięki  polu lookup_field = 'pk' w klasie
            return self.retrieve(request, *args, **kwargs ) #mixins.RetrieveModelMixin
        return self.list(request, *args, **kwargs) # metoda list pochodiz bezpośrednio z mixins.ListModelMixin,
    
    def post(self, request, *args, **kwargs): #HTTP method -> post
        # https://www.django-rest-framework.org/api-guide/generic-views/#createmodelmixin
        return self.create(request, *args, **kwargs) # mixins.CreateModelMixin

    def perform_create(self, serializer): # KOPIA metody z ProductListCreateAPIView(generics.ListCreateAPIView).perform_create(self, serializer):
        print(serializer.validated_data) # OrderedDict([('title', 'This field is done!'), ('price', Decimal('32.99'))])
        title = serializer.validated_data.get('title')
        content = serializer.validated_data.get('content') or None
        if content is None:
            content = 'tihs is a signle view doing cool stuff'

        instance = serializer.save(content=content)
        #wszystko dizała identycznie
        # OrderedDict([('title', 'This field is done!'), ('price', Decimal('32.99'))])
        # generics.ListCreateAPIView ma tę metodę perform_create(self, serializer) bo dziedziczy po mixins.CreateModelMixin
        # https://www.django-rest-framework.org/api-guide/generic-views/#listcreateapiview
        # https://www.django-rest-framework.org/api-guide/generic-views/#createapiview
