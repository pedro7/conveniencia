from django.urls import path

from . import views

urlpatterns = [
    path('', views.visualizar_usuarios, name='visualizar_usuarios'),
    path('cadastrar/', views.cadastrar_usuario, name='cadastrar_usuario'),
    path('editar/<str:nome_usuario>/', views.editar_usuario, name='editar_usuario'),
    path('excluir/<str:nome_usuario>/', views.excluir_usuario, name='excluir_usuario')
]
