from django.urls import path

from .views import (AumentarQuantidadeView, DiminuirQuantidadeView,
                    EstoqueListView)

urlpatterns = [
    path('', EstoqueListView.as_view(), name='visualizar_estoque'),
    path('<int:pk>/aumentar/', AumentarQuantidadeView.as_view(), name='aumentar_estoque'),
    path('<int:pk>/diminuir/', DiminuirQuantidadeView.as_view(), name='diminuir_estoque')
]
