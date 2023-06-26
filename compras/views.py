from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import redirect, render

from compras.models import Compra, CompraProduto


@login_required
def visualizar_compras(request: HttpRequest):
    total_compras = []
    compras = Compra.objects.all()
    for compra in compras:
        total = 0
        compra_produtos = CompraProduto.objects.filter(compra=compra)
        for compra_produto in compra_produtos:
            total += compra_produto.produto.preco * compra_produto.quantidade
        total_compras.append(total)
    compras = {k: v for k, v in zip(compras, total_compras)}
    return render(request, 'compras/compras.html', {'compras': compras})

@login_required
def excluir_compra(request: HttpRequest, id):
    Compra.objects.get(id=id).delete()
    return redirect('visualizar_compras')
