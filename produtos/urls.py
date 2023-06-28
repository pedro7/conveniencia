from django.urls import path

from . import views

urlpatterns = [
    path('', views.visualizar_produtos, name='visualizar_produtos'),
    path('cadastrar/', views.cadastrar_produto, name='cadastrar_produto'),
    path('<str:codigo_barras>/', views.visualizar_produto, name='visualizar_produto'),
    path('<str:codigo_barras>/editar/', views.editar_produto, name='editar_produto'),
    path('<str:codigo_barras>/excluir/', views.excluir_produto, name='excluir_produto')
]
