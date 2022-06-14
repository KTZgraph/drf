from django.urls import path

from . import views

urlpatterns = [
    #slash na końcu
    #path('sciezka/<typDanych:NazwaPola>/', widok
    path('<int:pk>/', views.ProductDetailAPIView.as_view())
]