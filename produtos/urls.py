from django.urls import path

from . import views

urlpatterns = [
    path('', views.visualizar_produtos, name='visualizar_produtos'),
    path('cadastrar/', views.cadastrar_produto, name='cadastrar_produto'),
    path('editar/<int:id>/', views.editar_produto, name='editar_produto'),
    path('excluir/<int:id>/', views.excluir_produto, name='excluir_produto')
]
