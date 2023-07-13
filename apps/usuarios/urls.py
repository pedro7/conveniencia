from django.urls import path

from .views import (UsuarioCreateView, UsuarioListView, UsuarioUpdateSenhaView,
                    UsuarioUpdateSituacaoView, UsuarioUpdateView, UsuarioUpdateAdministradorView)

urlpatterns = [
    path('', UsuarioListView.as_view(), name='visualizar_usuarios'),
    path('cadastrar/', UsuarioCreateView.as_view(), name='cadastrar_usuario'),
    path('<str:username>/editar/', UsuarioUpdateView.as_view(), name='editar_usuario'),
    path('<str:username>/editar-senha/', UsuarioUpdateSenhaView.as_view(), name='editar_senha_usuario'),
    path('<str:username>/alterar-administrador/', UsuarioUpdateAdministradorView.as_view(), name='alterar_administrador_usuario'),
    path('<str:username>/alterar-situacao/', UsuarioUpdateSituacaoView.as_view(), name='alterar_usuario_situacao')
]
