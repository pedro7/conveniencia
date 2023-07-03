from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import redirect, render

from apps.compras.models import Compra


@login_required
def visualizar_compras(request: HttpRequest):
    if not request.user.is_superuser:
        return redirect('entrar')
    valores_totais = []
    compras = Compra.objects.all()
    for compra in compras:
        total = 0
        for compra_produto in compra.compra_produtos.all():
            total += compra_produto.preco_unitario * compra_produto.quantidade
        valores_totais.append(total)
    compras_valores = {k: v for k, v in zip(compras, valores_totais)}
    return render(request, 'compras/compras.html', {'compras_valores': compras_valores})

@login_required
def excluir_compra(request: HttpRequest, id):
    if not request.user.is_superuser:
        return redirect('entrar')
    Compra.objects.get(id=id).delete()
    return redirect('visualizar_compras')
