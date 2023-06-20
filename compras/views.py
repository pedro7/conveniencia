from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from produtos.models import Produto


carrinho : list[Produto] = []

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