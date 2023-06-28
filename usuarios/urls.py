from django.urls import path

from . import views

urlpatterns = [
    path('', views.visualizar_usuarios, name='visualizar_usuarios'),
    path('cadastrar/', views.cadastrar_usuario, name='cadastrar_usuario'),
    path('<str:username>/', views.visualizar_usuario, name='visualizar_usuario'),
    path('<str:nome_usuario>/editar/', views.editar_usuario, name='editar_usuario'),
    path('<str:nome_usuario>/editar-senha/', views.editar_senha, name='editar_senha_usuario'),
    path('<str:nome_usuario>/excluir/', views.excluir_usuario, name='excluir_usuario')
]
