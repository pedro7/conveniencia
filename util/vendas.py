from datetime import date, timedelta

from django.utils import timezone

from apps.compras.models import Compra
from apps.produtos.models import Produto


def get_total_vendido_hoje():
    total_vendido_hoje = 0
    for compra in Compra.objects.filter(data__date=timezone.now().date()):
        for compra_produto in compra.compra_produtos.all():
            total_vendido_hoje += compra_produto.preco_unitario * compra_produto.quantidade
    return total_vendido_hoje

def get_produtos_mais_consumidos_hoje():
    produtos_mais_consumidos_hoje = {}
    for compra in Compra.objects.filter(data__date=timezone.now().date()):
        for compra_produto in compra.compra_produtos.all():
            if compra_produto.produto in produtos_mais_consumidos_hoje:
                produtos_mais_consumidos_hoje[compra_produto.produto] += compra_produto.quantidade
            else:
                produtos_mais_consumidos_hoje[compra_produto.produto] = compra_produto.quantidade
    return sorted(produtos_mais_consumidos_hoje.items(), key=lambda x: x[1], reverse=True)

def get_referencia_atual():
    data_hoje = date.today()
    if data_hoje.day >= 26:
        referencia_atual = data_hoje.replace(day=26)
    else:
        ultimo_dia_mes_passado = data_hoje.replace(day=1) - timedelta(days=1)
        referencia_atual = ultimo_dia_mes_passado.replace(day=26)
    return referencia_atual

def get_referencia_passada(referencia_atual):
    if referencia_atual.month == 1:
        referencia_passada = referencia_atual.replace(month=12, year=referencia_atual.year - 1)
    else:
        referencia_passada = referencia_atual.replace(month=referencia_atual.month - 1)
    return referencia_passada

def get_produtos_baixo_estoque():
    produtos_baixo_estoque = []
    for produto in Produto.objects.all():
        if produto.estoque.quantidade < 10:
            produtos_baixo_estoque.append(produto)
    return produtos_baixo_estoque