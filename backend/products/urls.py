from django.urls import path

from . import views

urlpatterns = [
    #slash na końcu
    #path('sciezka/<typDanych:NazwaPola>/', widok
    path('<int:pk>/', views.ProductDetailAPIView.as_view()),
    path('', views.product_list_create_view),
    # path('/', views.product_create_view),
    #sam slash TO ZLY POMYSŁ bo już mam path('api/products/'  ->  wtedy wyjdzie api/products//
]