 # account/urls.py
from django.urls import path
from . import views

urlpatterns = [

path('add_to_cart/', views.add_to_cart, name='add_to_cart'),  # Ensure the trailing slash
    path('cart/', views.show_cart, name='show_cart'),
    path('remove_from_cart/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('increment_quantity/<int:cart_item_id>/', views.increment_quantity, name='increment_quantity'),
    path('decrement_quantity/<int:cart_item_id>/', views.decrement_quantity, name='decrement_quantity'),
]