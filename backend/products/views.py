from types import GenericAlias


from rest_framework import generics


from .models import Product
from .serializers import ProductSerializer

class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    # można customowe queryset
    # def get_queryset(self):
    #     return super().get_queryset()
    serializer_class = ProductSerializer
    # gdy chce się detail view dla jednego konkretnego obiektu
    #lookup_field = 'pk <- podobnie jak Product.objects.get(pk=123)
