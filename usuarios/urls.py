from django.urls import path 
from .views import *

urlpatterns = [
    path('cadastro/', Cadastro, name= 'cadastro'),
    path('login/', Login, name= 'login'),
    path('logout/', Logout, name= 'logout'),
]