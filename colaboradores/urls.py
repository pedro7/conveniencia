from django.urls import path

from . import views

urlpatterns = [
    path('', views.colaboradores, name='colaboradores'),
    path('cadastrar/', views.cadastrar_colaborador, name='cadastrar_colaborador'),
    path('editar/<str:login>/', views.editar_colaborador, name='editar_colaborador'),
    path('ativar/<str:login>/', views.ativar_colaborador, name='ativar_colaborador'),
    path('inativar/<str:login>/', views.inativar_colaborador, name='inativar_colaborador')
]
