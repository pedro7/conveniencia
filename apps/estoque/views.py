from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView, ListView

from apps.movimentacoes.models import Movimentacao

from .forms import AlterarQuantidadeForm
from .models import Estoque


class EstoqueListView(LoginRequiredMixin, ListView):
    model = Estoque
    template_name = 'estoque/estoque.html'
    context_object_name = 'estoques'


class AumentarQuantidadeView(LoginRequiredMixin, FormView):
    form_class = AlterarQuantidadeForm
    template_name = 'base/editar.html'
    success_url = '/estoque/'

    def form_valid(self, form):
        estoque = Estoque.objects.get(pk=self.kwargs['pk'])
        estoque.quantidade += form.cleaned_data['quantidade']
        estoque.save()

        Movimentacao.objects.create(
            produto=estoque.produto,
            usuario=self.request.user,
            quantidade=form.cleaned_data['quantidade'],
            tipo='entrada'
        )

        return super().form_valid(form)
    

class DiminuirQuantidadeView(LoginRequiredMixin, FormView):
    form_class = AlterarQuantidadeForm
    template_name = 'base/editar.html'
    success_url = '/estoque/'

    def form_valid(self, form):
        estoque = Estoque.objects.get(pk=self.kwargs['pk'])
        estoque.quantidade -= form.cleaned_data['quantidade']
        estoque.save()

        Movimentacao.objects.create(
            produto=estoque.produto,
            usuario=self.request.user,
            quantidade=form.cleaned_data['quantidade'],
            tipo='saida'
        )

        return super().form_valid(form)
