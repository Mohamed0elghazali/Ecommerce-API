from django.urls import path 

from . import views

urlpatterns = [
    path('register/', views.register,  name='register'),
    path('userinfo/', views.user_info,  name='user_info'),
]