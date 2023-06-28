from collections import Counter
from datetime import date, timedelta

from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.http import HttpRequest
from django.shortcuts import redirect, render

from colaboradores.models import Colaborador
from compras.models import Compra
from produtos.models import Produto


carrinho: list[Produto] = []

def visualizar_carrinho(request: HttpRequest):
    total = 0
    for produto in carrinho:
        total += produto.preco
    context = {
        'carrinho': carrinho,
        'total': total
    }
    return render(request, 'carrinho/carrinho.html', context)

def adicionar_produto(request: HttpRequest):
    codigo_barras = request.POST['codigo_barras']
    try:
        produto = Produto.objects.get(codigo_barras=codigo_barras)
    except Produto.DoesNotExist:
        messages.error(request, 'Produto não cadastrado.')
        return redirect('visualizar_carrinho')
    carrinho.append(produto)
    return redirect('visualizar_carrinho')
    
def remover_produto(request: HttpRequest, posicao):
    carrinho.pop(posicao - 1)
    return redirect('visualizar_carrinho')
        
def esvaziar_carrinho(request: HttpRequest):
    carrinho.clear()
    return redirect('visualizar_carrinho')

def finalizar_compra(request: HttpRequest):
    colaborador = _get_colaborador_valido(request, request.POST['login'], request.POST['senha'])
    if not colaborador:
        return redirect('visualizar_carrinho')
    compra = Compra.objects.create(colaborador=colaborador)
    counter = Counter(carrinho)
    for produto, quantidade in counter.items():
        through_defaults = {
            'quantidade': quantidade,
            'preco_unitario': produto.preco
        }
        compra.produtos.add(produto, through_defaults=through_defaults)
    carrinho.clear()
    return redirect('visualizar_carrinho')

def consultar_gasto_mensal(request: HttpRequest):
    colaborador = _get_colaborador_valido(request, request.POST['login'], request.POST['senha'])
    if not colaborador:
        return redirect('visualizar_carrinho')
    gasto_referencia_atual = 0
    referencia_atual = _get_referencia_atual()
    for compra in Compra.objects.filter(colaborador=colaborador, data__gte=referencia_atual):
        for compra_produto in compra.compra_produtos.all():
            gasto_referencia_atual += compra_produto.preco_unitario * compra_produto.quantidade
    gasto_referencia_passada = 0
    for compra in Compra.objects.filter(colaborador=colaborador, data__range=[_get_referencia_passada(referencia_atual), referencia_atual]):
        for compra_produto in compra.compra_produtos.all():
            gasto_referencia_passada += compra_produto.preco_unitario * compra_produto.quantidade
    context = {
        'carrinho': carrinho,
        'gasto_mensal': gasto_referencia_atual,
        'gasto_referencia_passada': gasto_referencia_passada
    }
    return render(request, 'carrinho/carrinho.html', context)

def _get_colaborador_valido(request, login, senha):
    try:
        colaborador = Colaborador.objects.get(login=login)
    except Colaborador.DoesNotExist:
        messages.error(request, 'Colaborador não cadastrado.')
        return None
    if colaborador.situacao == 'inativo':
        messages.error(request, 'Colaborador inativo.')
        return None
    if not check_password(senha, colaborador.senha):
        messages.error(request, 'Senha incorreta.')
        return None
    return colaborador

def _get_referencia_atual():
    data_hoje = date.today()
    if data_hoje.day >= 26:
        referencia_atual = data_hoje.replace(day=26)
    else:
        ultimo_dia_mes_passado = data_hoje.replace(day=1) - timedelta(days=1)
        referencia_atual = ultimo_dia_mes_passado.replace(day=26)
    return referencia_atual

def _get_referencia_passada(referencia_atual):
    if referencia_atual.month == 1:
        referencia_passada = referencia_atual.replace(month=12, year=referencia_atual.year - 1)
    else:
        referencia_passada = referencia_atual.replace(month=referencia_atual.month - 1)
    return referencia_passada