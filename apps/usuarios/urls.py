from django.urls import path

from .views import (UsuarioCreateView, UsuarioDeleteView, UsuarioDetailView,
                    UsuarioListView, UsuarioUpdateView)

urlpatterns = [
    path('', UsuarioListView.as_view(), name='visualizar_usuarios'),
    path('cadastrar/', UsuarioCreateView.as_view(), name='cadastrar_usuario'),
    path('<str:username>/', UsuarioDetailView.as_view(), name='visualizar_usuario'),
    path('<str:nome_usuario>/editar/', UsuarioUpdateView.as_view(), name='editar_usuario'),
    path('<str:nome_usuario>/excluir/', UsuarioDeleteView.as_view(), name='excluir_usuario')
]
