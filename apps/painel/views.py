from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, RedirectView

from apps.compras.models import Compra
from common.util.vendas import (get_produtos_mais_consumidos_hoje,
                                get_total_vendido_hoje)


class PainelView(LoginRequiredMixin, ListView):
    model = Compra
    template_name = 'painel/painel.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['total_vendido_hoje'] = get_total_vendido_hoje()
        context['produtos_mais_consumidos_hoje'] = get_produtos_mais_consumidos_hoje()
        return context


class RedirecionarPainelView(LoginRequiredMixin, RedirectView):
    url = 'visualizar_painel'
