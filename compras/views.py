from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from produtos.models import Produto
from colaboradores.models import Colaborador
from compras.models import Compra


carrinho: list[Produto] = []

def compras(request: HttpRequest):
    total = 0
    for produto in carrinho:
        total += produto.preco
    context = {
        'carrinho': carrinho,
        'total': total
    }
    return render(request, 'compras/compras.html', context)

def adicionar_produto(request: HttpRequest):
    codigo_barras = request.POST['codigo_barras']
    produto = Produto.objects.get(codigo_barras=codigo_barras)
    carrinho.append(produto)
    return redirect('compras')
    
def remover_produto(request: HttpRequest, codigo_barras):
    for produto in carrinho:
        if produto.codigo_barras == codigo_barras:
            carrinho.remove(produto)
            return redirect('compras')
        
def limpar_carrinho(request: HttpRequest):
    carrinho.clear()
    return redirect('compras')

def finalizar(request: HttpRequest):
    if request.method == 'POST':
        login = request.POST['login']
        senha = request.POST['senha']
        colaborador = Colaborador.objects.get(login=login)
        compra = Compra.objects.create(colaborador=colaborador)
        compra.produtos.set(carrinho)
    return redirect('compras')
        