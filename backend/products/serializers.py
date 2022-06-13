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
        # do pola my_discount
        print(obj.id)
        # gdy mam usera obj.user -> user.username to mogę pobrac usera
        # gdy mam relacje z kluczami to mogę pobrac dane z innej tabeli/modelu
        # obj.category -> 
        return obj.get_discount()

# można mieć więcej serializerow  do  jednego modelu jeśli jest taka potrzeba
# class SecondaryProductSerializer(serializers.ModelSerializer):
#     my_discount = serializers.SerializerMethodField(read_only=True)
#     class Meta:
#         model = Product
#         fields = [
#             'title',
#             'content',
#             'price',
#             'sale_price', #property z modelu
#             'get_discount', #metoda z modelu
#             'my_discount', #takieg czegoś nie ma modelu
#         ]

#     def get_my_discount(self, obj): #get_moje_dynamiczne_pole_w_serializerze - bedzie w zwrotce widozne u klienta
#         # do pola my_discount
#         print(obj.id)
#         # gdy mam usera obj.user -> user.username to mogę pobrac usera
#         # gdy mam relacje z kluczami to mogę pobrac dane z innej tabeli/modelu
#         # obj.category -> 
#         return obj.get_discount()