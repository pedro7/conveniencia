from django.urls import path

from . import views

urlpatterns = [
    path('', views.visualizar_carrinho, name='visualizar_carrinho'),
    path('adicionar/', views.adicionar_produto, name='adicionar_produto'),
    path('remover/<int:posicao>/', views.remover_produto, name='remover_produto'),
    path('esvaziar/', views.esvaziar_carrinho, name='esvaziar_carrinho'),
    path('finalizar/', views.finalizar_compra, name='finalizar_compra'),
    path('consultar-gasto-mensal/', views.consultar_gasto_mensal, name='consultar_gasto_mensal')
]
