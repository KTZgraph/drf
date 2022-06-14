from django.urls import path, include

from . import views #from .views import api_home

urlpatterns = [
    path('', views.api_home),
    #1:33:43
    #jak jest dużo widoków które robią standardowe rzeczy django to dobrze w jednym trzymać wszystkie endpointy
    # path('products/', include('products.urls')), 

]