from django.urls import path

from .views import UsuarioCreateView, UsuarioListView, UsuarioUpdateView

urlpatterns = [
    path('', UsuarioListView.as_view(), name='visualizar_usuarios'),
    path('cadastrar/', UsuarioCreateView.as_view(), name='cadastrar_usuario'),
    path('<str:username>/editar/', UsuarioUpdateView.as_view(), name='editar_usuario'),
]
