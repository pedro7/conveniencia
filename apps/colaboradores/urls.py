from django.urls import path

from .views import (ColaboradorCreateView, ColaboradorListView,
                    ColaboradorUpdateView)

urlpatterns = [
    path('', ColaboradorListView.as_view(), name='visualizar_colaboradores'),
    path('cadastrar/', ColaboradorCreateView.as_view(), name='cadastrar_colaborador'),
    path('<str:login>/editar/', ColaboradorUpdateView.as_view(), name='editar_colaborador'),
]
