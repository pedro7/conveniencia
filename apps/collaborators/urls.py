from django.urls import path

from . import views

urlpatterns = [
    path('', views.CollaboratorListView.as_view(), name='visualizar_colaboradores'),
    path('cadastrar/', views.CollaboratorCreateView.as_view(), name='cadastrar_colaborador'),
    path('<str:login>/', views.visualizar_colaborador, name='visualizar_colaborador'),
    path('<str:login>/editar/', views.editar_colaborador, name='editar_colaborador'),
    path('<str:login>/editar-senha/', views.editar_senha, name='editar_senha_colaborador'),
    path('<str:login>/alterar-situacao/', views.alterar_situacao, name='alterar_situacao')
]
