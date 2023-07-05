from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView

from .models import Produto


class ProdutoListView(ListView):
    model = Produto
    template_name = 'produtos/produtos.html'
    context_object_name = 'produtos'


class ProdutoCreateView(CreateView):
    model = Produto
    fields = '__all__'
    template_name = 'produtos/cadastrar_produto.html'
    success_url = '/produtos/'


class ProdutoDetailView(DetailView):
    model = Produto
    template_name = 'produtos/produto.html'
    context_object_name = 'produto'
    slug_field = 'codigo_barras'
    slug_url_kwarg = 'codigo_barras'


class ProdutoUpdateView(UpdateView):
    model = Produto
    fields = '__all__'
    template_name = 'produtos/cadastrar_produto.html'
    success_url = '/produtos/'
    slug_field = 'codigo_barras'
    slug_url_kwarg = 'codigo_barras'
