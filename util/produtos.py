from datetime import timezone

from apps.compras.models import Compra
from apps.produtos.models import Produto


def get_produtos_mais_consumidos_hoje():
    produtos_mais_consumidos_hoje = {}
    for compra in Compra.objects.filter(data__date=timezone.now().date()):
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