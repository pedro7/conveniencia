from django.views.generic import ListView

from .models import Movimentacao


class MovimentacoesListView(ListView):
    model = Movimentacao
    template_name = 'movimentacoes/movimentacoes.html'
    context_object_name = 'movimentacoes'
