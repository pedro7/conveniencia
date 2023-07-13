from django.urls import path

from .views import (ColaboradorCreateView, ColaboradorListView,
                    ColaboradorUpdateSenhaView, ColaboradorUpdateSituacaoView,
                    ColaboradorUpdateView)

urlpatterns = [
    path('', ColaboradorListView.as_view(), name='visualizar_colaboradores'),
    path('cadastrar/', ColaboradorCreateView.as_view(), name='cadastrar_colaborador'),
    path('<str:login>/editar/', ColaboradorUpdateView.as_view(), name='editar_colaborador'),
    path('<str:login>/editar-senha/', ColaboradorUpdateSenhaView.as_view(), name='editar_senha_colaborador'),
    path('<str:login>/alterar-situacao/', ColaboradorUpdateSituacaoView.as_view(), name='alterar_situacao_colaborador')
]
