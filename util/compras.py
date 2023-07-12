from collections import Counter

from django.utils import timezone

from apps.compras.models import Compra
from util.emails import enviar_email_compra_ingresso, enviar_email_compra_roupa

from .estoque import diminuir_estoque
from .referencias import get_referencia_atual, get_referencia_passada


def cadastrar_compra(colaborador, produtos):
    compra = Compra.objects.create(colaborador=colaborador)
    produtos = Counter(produtos)
    for produto, quantidade in produtos.items():
        through_defaults = {
            'quantidade': quantidade,
            'preco_unitario': produto.preco
        }
        compra.produtos.add(produto, through_defaults=through_defaults)
        if produto.tipo == 'ingresso':
            enviar_email_compra_ingresso(colaborador, quantidade)
        else:
            diminuir_estoque(produto, quantidade)
        if produto.tipo == 'roupa':
            enviar_email_compra_roupa(colaborador, quantidade)
        else:
            diminuir_estoque(produto, quantidade)

def get_total_vendido_hoje():
    total_vendido_hoje = 0
    for compra in Compra.objects.filter(data__date=timezone.now().date()):
        for compra_produto in compra.compra_produtos.all():
            total_vendido_hoje += compra_produto.preco_unitario * compra_produto.quantidade
    return total_vendido_hoje

def get_gasto_referencia_atual_colaborador(colaborador):
    gasto_referencia_atual = 0
    for compra in Compra.objects.filter(colaborador=colaborador, data__gte=get_referencia_atual()):
        for compra_produto in compra.compra_produtos.all():
            gasto_referencia_atual += compra_produto.preco_unitario * compra_produto.quantidade
    return gasto_referencia_atual

def get_gasto_referencia_passada_colaborador(colaborador):
    gasto_referencia_passada = 0
    for compra in Compra.objects.filter(colaborador=colaborador, data__range=[get_referencia_passada(), get_referencia_atual()]):
        for compra_produto in compra.compra_produtos.all():
            gasto_referencia_passada += compra_produto.preco_unitario * compra_produto.quantidade
    return gasto_referencia_passada