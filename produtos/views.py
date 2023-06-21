from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from .models import Produto


@login_required
def visualizar_produtos(request: HttpRequest):
    if request.method == 'GET':
        produtos = Produto.objects.all()
        return render(request, 'produtos/produtos.html', {'produtos': produtos})

@login_required
def cadastrar_produto(request: HttpRequest):
    if request.method == 'POST':
        nome = request.POST['nome']
        codigo_barras = request.POST['codigo_barras']
        preco = request.POST['preco']
        Produto.objects.create(nome=nome, codigo_barras=codigo_barras, preco=preco)
        return redirect('visualizar_produtos')
    
@login_required
def editar_produto(request: HttpRequest, id):
    produto = Produto.objects.get(id=id)
    if request.method == 'GET':
        return render(request, 'produtos/editar-produto.html', {'produto': produto})
    elif request.method == 'POST':
        produto.nome = request.POST['nome']
        produto.codigo_barras = request.POST['codigo_barras']
        produto.preco = request.POST['preco']
        produto.save()
        return redirect('visualizar_produtos')

@login_required
def excluir_produto(request: HttpRequest, id):
    if request.method == 'POST':
        Produto.objects.get(id=id).delete()
        return redirect('visualizar_produtos')
