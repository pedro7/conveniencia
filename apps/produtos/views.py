from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views import View
from django.views.generic import CreateView, ListView, UpdateView

from apps.estoque.models import Estoque

from .models import Produto


class ProdutoListView(LoginRequiredMixin, ListView):
    model = Produto
    template_name = 'produtos/produtos.html'
    context_object_name = 'produtos'


class ProdutoCreateView(LoginRequiredMixin, CreateView):
    model = Produto
    fields = ['nome', 'codigo_barras', 'preco', 'tipo']
    template_name = 'base/cadastrar.html'
    success_url = '/produtos/'

    def form_valid(self, form):
        produto = form.save()
        Estoque.objects.create(produto=produto)
        return redirect('visualizar_produtos')


class ProdutoUpdateView(LoginRequiredMixin, UpdateView):
    model = Produto
    fields = '__all__'
    template_name = 'base/editar.html'
    success_url = '/produtos/'
    slug_field = 'codigo_barras'
    slug_url_kwarg = 'codigo_barras'


class ProdutoUpdateSituacaoView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        produto = Produto.objects.get(codigo_barras=kwargs['codigo_barras'])
        if produto.situacao == 'ativo':
            produto.situacao = 'inativo'
        else:
            produto.situacao = 'ativo'
        produto.save()
        return redirect('visualizar_produtos')
