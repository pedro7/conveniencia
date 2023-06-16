from django.urls import path

from . import views

urlpatterns = [
    path('', views.colaboradores, name='colaboradores'),
    path('cadastrar/', views.cadastrar_colaborador, name='cadastrar_colaborador'),
    path('editar/<str:login>/', views.editar_colaborador, name='editar_colaborador'),
    path('excluir/<str:login>/', views.excluir_colaborador, name='excluir_colaborador')
]
