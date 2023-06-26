from django.urls import path

from . import views

urlpatterns = [
    path('', views.visualizar_colaboradores, name='visualizar_colaboradores'),
    path('cadastrar/', views.cadastrar_colaborador, name='cadastrar_colaborador'),
    path('editar/<str:login>/', views.editar_colaborador, name='editar_colaborador'),
    path('alterar-situacao/<str:login>/', views.alterar_situacao, name='alterar_situacao')
]
