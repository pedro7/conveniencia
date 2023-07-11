from django.urls import path

from .views import MovimentacoesListView

urlpatterns = [
    path('', MovimentacoesListView.as_view(), name='visualizar_movimentacoes')
]
