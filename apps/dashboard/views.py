from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.utils import timezone

from apps.purchases.models import Purchase


@login_required
def visualizar_painel(request: HttpRequest):
    total_vendido_hoje = _get_total_vendido_hoje()
    produtos_mais_consumidos_hoje = _get_produtos_mais_consumidos_hoje()
    context = {
        'total_vendido_hoje': total_vendido_hoje,
        'produtos_mais_consumidos_hoje': produtos_mais_consumidos_hoje
    }
    return render(request, 'painel/painel.html', context)

def _get_total_vendido_hoje():
    total_vendido_hoje = 0
    for compra in Purchase.objects.filter(date__date=timezone.now().date()):
        for compra_produto in compra.purchase_products.all():
            total_vendido_hoje += compra_produto.unit_price * compra_produto.quantity
    return total_vendido_hoje

def _get_produtos_mais_consumidos_hoje():
    produtos_mais_consumidos_hoje = {}
    for compra in Purchase.objects.filter(date__date=timezone.now().date()):
        for compra_produto in compra.purchase_products.all():
            if compra_produto.product in produtos_mais_consumidos_hoje:
                produtos_mais_consumidos_hoje[compra_produto.product] += compra_produto.quantity
            else:
                produtos_mais_consumidos_hoje[compra_produto.product] = compra_produto.quantity
    return sorted(produtos_mais_consumidos_hoje.items(), key=lambda x: x[1], reverse=True)

@login_required
def redirecionar_painel(request: HttpRequest):
    return redirect('visualizar_painel')
