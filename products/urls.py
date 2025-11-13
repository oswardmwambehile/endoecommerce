# account/urls.py
from django.urls import path
from . import views

urlpatterns = [
    
    path('product-list/', views.products, name='product-lists'),
    path('get-attributes/', views.get_attributes, name='get_attributes'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('category/<str:pk>', views.category, name='category'),
]
