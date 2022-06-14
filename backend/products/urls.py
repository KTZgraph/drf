from django.urls import path

from . import views

urlpatterns = [
    path('mixin/', views.ProductMixinView.as_view()), # [2:07:30] około
    #slash na końcu
    #path('sciezka/<typDanych:NazwaPola>/', widok
    path('<int:pk>/', views.ProductDetailAPIView.as_view()),
    path('mixin/<int:pk>/', views.ProductMixinView.as_view()), #[2:1023]
    path('', views.product_list_create_view),
    # path('/', views.product_create_view),
    #sam slash TO ZLY POMYSŁ bo już mam path('api/products/'  ->  wtedy wyjdzie api/products//
    path('alt/<int:pk>/', views.product_alt_view), #wszystko robi jedna klasa - tworzy i listuje poejdyncyz i wszzsytkie obiekty List, Read, Create
    # 1:55:40 UpdateApiView & DestroyAPIView
    path('<int:pk>/update/', views.ProductUpdateAPIView.as_view()),
    path('<int:pk>/delete/', views.ProductDestroyAPIView.as_view()),

]