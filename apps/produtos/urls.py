from django.urls import path

from .views import (ProdutoCreateView, ProdutoDetailView, ProdutoListView,
                    ProdutoUpdateView)

urlpatterns = [
    path('', ProdutoListView.as_view(), name='visualizar_produtos'),
    path('cadastrar/', ProdutoCreateView.as_view(), name='cadastrar_produto'),
    path('<str:codigo_barras>/', ProdutoDetailView.as_view(), name='visualizar_produto'),
    path('<str:codigo_barras>/editar/', ProdutoUpdateView.as_view(), name='editar_produto')
]
