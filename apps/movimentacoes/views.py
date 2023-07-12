from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from .models import Movimentacao


class MovimentacoesListView(LoginRequiredMixin, ListView):
    model = Movimentacao
    template_name = 'movimentacoes/movimentacoes.html'
    context_object_name = 'movimentacoes'
