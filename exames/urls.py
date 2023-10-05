from django.urls import path
from .views import *

urlpatterns = [
    path('solicitar_exames/', Solicitar_exames, name='solicitar_exames'),
    path('fechar_pedido/', Fechar_pedido, name='fechar_pedido'),
]
