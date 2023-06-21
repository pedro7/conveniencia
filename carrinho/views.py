from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from produtos.models import Produto
from colaboradores.models import Colaborador
from compras.models import Compra
from collections import Counter


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
    produto = Produto.objects.get(codigo_barras=codigo_barras)
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
        colaborador = Colaborador.objects.get(login=login)
        counter = Counter(carrinho)
        compra = Compra.objects.create(colaborador=colaborador)
        for produto, quantidade in counter.items():
            compra.produtos.add(produto, through_defaults={'quantidade': quantidade})
        carrinho.clear()
    return redirect('visualizar_carrinho')
        