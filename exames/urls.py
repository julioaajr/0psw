from django.urls import path
from .views import *

urlpatterns = [
    path('solicitar_exames/', Solicitar_exames, name='solicitar_exames'),
    path('fechar_pedido/', Fechar_pedido, name='fechar_pedido'),
    path('gerenciar_pedidos/', Gerenciar_pedidos, name="gerenciar_pedidos"),
    path('cancelar_pedido/<int:pedido_id>', Cancelar_pedido, name= 'cancelar_pedido'),
    path('gerenciar_exames/', Gerenciar_exames, name= 'gerenciar_exames'),
]
