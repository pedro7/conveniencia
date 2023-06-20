from django.urls import path

from . import views

urlpatterns = [
    path('', views.compras, name='compras'),
    path('adicionar/', views.adicionar_produto, name='adicionar_produto'),
    path('remover/<str:codigo_barras>/', views.remover_produto, name='remover_produto'),
    path('limpar/', views.limpar_carrinho, name='limpar_carrinho')
]
