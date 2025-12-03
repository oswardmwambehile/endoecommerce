# account/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # example
    path('dash/', views.home, name='index'),
     path('register/', views.register, name='register'),
     path('login/', views.login_user, name='login'),
     path('logout',views.logout_user, name='logout'),
     path('change-password/', views.change_password, name='change_password'), 
     path('profile/', views.profile_view, name='profile'),

]
