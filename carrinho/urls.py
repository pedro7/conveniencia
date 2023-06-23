from django.urls import path

from . import views

urlpatterns = [
    path('', views.visualizar_carrinho, name='visualizar_carrinho'),
    path('adicionar/', views.adicionar_produto, name='adicionar_produto'),
    path('remover/<int:index>/', views.remover_produto, name='remover_produto'),
    path('limpar/', views.limpar_carrinho, name='limpar_carrinho'),
    path('finalizar/', views.finalizar_compra, name='finalizar_compra'),
    path('consultar/', views.consultar_gastos, name='consultar_gastos')
]
