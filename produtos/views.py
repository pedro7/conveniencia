from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import ProtectedError
from django.http import HttpRequest
from django.shortcuts import redirect, render

from .models import Produto, ProdutoForm


@login_required
def visualizar_produtos(request: HttpRequest):
    produtos = Produto.objects.all()
    return render(request, 'produtos/produtos.html', {'produtos': produtos})

@login_required
def cadastrar_produto(request: HttpRequest):
    form = ProdutoForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect('visualizar_produtos')
    for error_list in form.errors.values():
        for error in error_list:
            messages.error(request, error)
    return redirect('visualizar_produtos')
    
@login_required
def editar_produto(request: HttpRequest, codigo_barras):
    produto = Produto.objects.get(codigo_barras=codigo_barras)
    if request.method == 'GET':
        return render(request, 'produtos/editar-produto.html', {'produto': produto})
    form = ProdutoForm(request.POST, instance=produto)
    if form.is_valid():
        form.save()
        return redirect('visualizar_produtos')
    for error_list in form.errors.values():
        for error in error_list:
            messages.error(request, error)
    return render(request, 'produtos/editar-produto.html', {'produto': produto})

@login_required
def excluir_produto(request: HttpRequest, codigo_barras):
    try:
        Produto.objects.get(codigo_barras=codigo_barras).delete()
    except ProtectedError:
        messages.error(request, 'Não é possível excluir pois o produto está vinculado a uma ou mais compras.')
    return redirect('visualizar_produtos')
