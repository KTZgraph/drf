from tkinter.messagebox import NO
from rest_framework import serializers

from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    #serilizery też mogą czyścić i walidować dane czy są poprawne
    my_discount = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Product
        fields = [
            'title',
            'content',
            'price',
            'sale_price', #property z modelu
            'get_discount', #metoda z modelu
            'my_discount', #takieg czegoś nie ma modelu
        ]

    def get_my_discount(self, obj): #get_moje_dynamiczne_pole_w_serializerze - bedzie w zwrotce widozne u klienta
        if not hasattr(obj, 'id'):
            return None
        if not isinstance(obj, Product):
            return None
        return obj.get_discount()

        # bez try - except lub if not hasattr(obj, 'id'): lub if not isinstance(obj, Product):
        # return obj.get_discount()
        # AttributeError: 'collections.OrderedDict' object has no attribute 'get_discount'
