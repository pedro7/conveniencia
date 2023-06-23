from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import redirect, render

from .models import Produto, ProdutoForm


@login_required
def visualizar_produtos(request: HttpRequest):
    if request.method == 'GET':
        produtos = Produto.objects.all()
        return render(request, 'produtos/produtos.html', {'produtos': produtos})

@login_required
def cadastrar_produto(request: HttpRequest):
    if request.method == 'POST':
        form = ProdutoForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            for error_list in form.errors.values():
                for error in error_list:
                    messages.error(request, error)
        return redirect('visualizar_produtos')
    
@login_required
def editar_produto(request: HttpRequest, id):
    produto = Produto.objects.get(id=id)
    if request.method == 'GET':
        return render(request, 'produtos/editar-produto.html', {'produto': produto})
    elif request.method == 'POST':
        form = ProdutoForm(request.POST, instance=produto)
        if form.is_valid():
            form.save()
        else:
            for error_list in form.errors.values():
                for error in error_list:
                    messages.error(request, error)
            return render(request, 'produtos/editar-produto.html', {'produto': produto})
        return redirect('visualizar_produtos')

@login_required
def excluir_produto(request: HttpRequest, id):
    if request.method == 'POST':
        Produto.objects.get(id=id).delete()
        return redirect('visualizar_produtos')
