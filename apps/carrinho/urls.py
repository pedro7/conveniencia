from django.urls import path

from .views import (AdicionarProdutoView, CarrinhoView,
                    ConsultarGastoMensalView, EsvaziarCarrinhoView,
                    FinalizarCompraView, RemoverProdutoView)

urlpatterns = [
    path('', CarrinhoView.as_view(), name='visualizar_carrinho'),
    path('adicionar/', AdicionarProdutoView.as_view(), name='adicionar_produto'),
    path('remover/<int:posicao>/', RemoverProdutoView.as_view(), name='remover_produto'),
    path('esvaziar/', EsvaziarCarrinhoView.as_view(), name='esvaziar_carrinho'),
    path('finalizar/', FinalizarCompraView.as_view(), name='finalizar_compra'),
    path('consultar-gasto-mensal/', ConsultarGastoMensalView.as_view(), name='consultar_gasto_mensal')
]
