from types import GenericAlias


from rest_framework import generics


from .models import Product
from .serializers import ProductSerializer

class ProductCreateAPIView(generics.CreateAPIView):
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
product_create_view = ProductCreateAPIView.as_view()

class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    # można customowe queryset
    # def get_queryset(self):
    #     return super().get_queryset()
    serializer_class = ProductSerializer
    # gdy chce się detail view dla jednego konkretnego obiektu
    #lookup_field = 'pk <- podobnie jak Product.objects.get(pk=123)
