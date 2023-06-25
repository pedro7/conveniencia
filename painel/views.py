from datetime import datetime
from django.utils import timezone

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from reportlab.pdfgen.canvas import Canvas

from colaboradores.models import Colaborador
from compras.models import Compra, CompraProduto


@login_required
def visualizar_painel(request: HttpRequest):
    total_hoje = get_venda_diaria()
    produtos_mais_consumidos = get_produtos_mais_consumidos()
    context = {
        'total_hoje': total_hoje,
        'produtos_mais_consumidos': produtos_mais_consumidos
    }
    return render(request, 'painel/painel.html', context)

def get_venda_diaria():
    today = timezone.now().date()
    total_hoje = 0
    for compra in Compra.objects.filter(data__date=today):
        for produto in compra.produtos.all():
            total_hoje += produto.preco
    return total_hoje

def get_produtos_mais_consumidos():
    produtos_mais_consumidos = {}
    today = timezone.now().date()
    for compra in Compra.objects.filter(data__date=today):
        compra_produtos = CompraProduto.objects.filter(compra=compra)
        for compra_produto in compra_produtos:
            produto = compra_produto.produto
            if produto in produtos_mais_consumidos:
                produtos_mais_consumidos[produto] += compra_produto.quantidade
            else:
                produtos_mais_consumidos[produto] = compra_produto.quantidade
    return sorted(produtos_mais_consumidos.items(), key=lambda x: x[1], reverse=True)

    