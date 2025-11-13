from django.urls import path
from . import views

urlpatterns = [
    
 path('checkout',views.checkout, name='checkout'),
  path('order-success/', views.order_success, name='order_success'),
    path('order-progress/', views.order_progress, name='order-progress'),
    path('download-order-pdf/', views.download_order_pdf, name='download_order_pdf'),
]