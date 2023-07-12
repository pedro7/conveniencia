from datetime import datetime

from django.contrib.messages import error

from apps.compras.models import Compra
from apps.produtos.models import Produto


def get_produto_valido(request, codigo_barras):
    try:
        produto = Produto.objects.get(codigo_barras=codigo_barras)
    except Produto.DoesNotExist:
        error(request, 'Produto não encontrado.')
        return None
    if produto.situacao == 'inativo':
        error(request, 'Produto inativo.')
        return None
    else:
        return produto

def get_produtos_mais_consumidos_hoje():
    produtos_mais_consumidos_hoje = {}
    for compra in Compra.objects.filter(data__date=datetime.now().date()):
        for compra_produto in compra.compra_produtos.all():
            if compra_produto.produto in produtos_mais_consumidos_hoje:
                produtos_mais_consumidos_hoje[compra_produto.produto] += compra_produto.quantidade
            else:
                produtos_mais_consumidos_hoje[compra_produto.produto] = compra_produto.quantidade
    return sorted(produtos_mais_consumidos_hoje.items(), key=lambda x: x[1], reverse=True)

def get_produtos_baixo_estoque():
    produtos_baixo_estoque = []
    for produto in Produto.objects.all():
        if produto.estoque.quantidade < 4 and produto.situacao == 'ativo':
            produtos_baixo_estoque.append(produto)
    return produtos_baixo_estoque