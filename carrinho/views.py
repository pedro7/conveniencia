from collections import Counter

from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.http import HttpRequest
from django.shortcuts import redirect, render

from colaboradores.models import Colaborador
from compras.models import Compra, CompraProduto
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
    
def remover_produto(request: HttpRequest, index):
    carrinho.pop(index - 1)
    return redirect('visualizar_carrinho')
        
def limpar_carrinho(request: HttpRequest):
    carrinho.clear()
    return redirect('visualizar_carrinho')

def finalizar_compra(request: HttpRequest):
    if request.method == 'POST':
        login = request.POST['login']
        senha = request.POST['senha']
        try:
            colaborador = Colaborador.objects.get(login=login)
        except Colaborador.DoesNotExist:
            messages.error(request, 'Colaborador não cadastrado.')
            return redirect('visualizar_carrinho')
        if colaborador.situacao == 'inativo':
            messages.error(request, 'Colaborador inativo.')
            return redirect('visualizar_carrinho')
        if not check_password(senha, colaborador.senha):
            messages.error(request, 'Senha incorreta.')
            return redirect('visualizar_carrinho')
        counter = Counter(carrinho)
        compra = Compra.objects.create(colaborador=colaborador)
        for produto, quantidade in counter.items():
            compra.produtos.add(produto, through_defaults={'quantidade': quantidade})
        carrinho.clear()
    return redirect('visualizar_carrinho')

def consultar_gastos(request: HttpRequest):
    if request.method == 'POST':
        login = request.POST['login']
        senha = request.POST['senha']
        try:
            colaborador = Colaborador.objects.get(login=login)
        except Colaborador.DoesNotExist:
            messages.error(request, 'Colaborador não cadastrado.')
            return redirect('visualizar_carrinho')
        if colaborador.situacao == 'inativo':
            messages.error(request, 'Colaborador inativo.')
            return redirect('visualizar_carrinho')
        if not check_password(senha, colaborador.senha):
            messages.error(request, 'Senha incorreta.')
            return redirect('visualizar_carrinho')
        compras = Compra.objects.filter(colaborador=colaborador)
        total_gasto = 0
        for compra in compras:
            compra_produtos = CompraProduto.objects.filter(compra=compra)
            for compra_produto in compra_produtos:
                produto = Produto.objects.get(id=compra_produto.produto.id)
                total_gasto += produto.preco * compra_produto.quantidade
        return render(request, 'carrinho/carrinho.html', {'total_gasto': total_gasto})
