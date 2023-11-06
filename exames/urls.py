from django.urls import path
from .views import *

urlpatterns = [
    path('solicitar_exames/', Solicitar_exames, name='solicitar_exames'),
    path('fechar_pedido/', Fechar_pedido, name='fechar_pedido'),
    path('gerenciar_pedidos/', Gerenciar_pedidos, name="gerenciar_pedidos"),
    path('cancelar_pedido/<int:pedido_id>', Cancelar_pedido, name= 'cancelar_pedido'),
    path('gerenciar_exames/', Gerenciar_exames, name= 'gerenciar_exames'),
    path('permitir_abrir_exame/<int:exame_id>', Permitir_abrir_exame, name= 'permitir_abrir_exame'),
    path('solicitar_senha_exame/<int:exame_id>', Solicitar_senha_exame, name="solicitar_senha_exame"),
]
