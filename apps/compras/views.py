from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import DeleteView, DetailView, ListView

from apps.compras.models import Compra


class CompraListView(UserPassesTestMixin, ListView):
    model = Compra
    template_name = 'compras/compras.html'
    context_object_name = 'compras_valores'

    def test_func(self):
        return self.request.user.is_superuser

    def get_queryset(self):
        if not self.request.user.is_superuser:
            return Compra.objects.none()
        
        compras = super().get_queryset()
        valores_totais = []
        for compra in compras:
            total = 0
            for compra_produto in compra.compra_produtos.all():
                total += compra_produto.preco_unitario * compra_produto.quantidade
            valores_totais.append(total)
        compras_valores = {k: v for k, v in zip(compras, valores_totais)}
        return compras_valores


class CompraDetailView(UserPassesTestMixin, DetailView):
    model = Compra
    template_name = 'compras/compra-produtos.html'
    context_object_name = 'compra'

    def test_func(self):
        return self.request.user.is_superuser


class CompraDeleteView(UserPassesTestMixin, DeleteView):
    model = Compra
    template_name = 'base/deletar.html'
    success_url = '/compras/'

    def test_func(self):
        return self.request.user.is_superuser
