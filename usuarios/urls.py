from django.urls import path

from . import views

urlpatterns = [
    path('entrar/', views.entrar, name='entrar'),
    path('sair/', views.sair, name='sair'),
    path('usuarios/', views.usuarios, name='usuarios'),
    path('usuarios/cadastrar/', views.cadastrar_usuario, name='cadastrar_usuario'),
    path('usuarios/editar/<str:nome_usuario>/', views.editar_usuario, name='editar_usuario'),
    path('usuarios/excluir/<str:nome_usuario>/', views.excluir_usuario, name='excluir_usuario')
]
