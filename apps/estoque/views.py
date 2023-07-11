from django.forms import ValidationError
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.views.generic import ListView, UpdateView

from .models import Estoque


class EstoqueListView(ListView):
    model = Estoque
    template_name = 'estoque/estoque.html'
    context_object_name = 'estoques'

class EstoqueUpdateView(UpdateView):
    model = Estoque
    fields = ['quantidade']
    template_name = 'editar.html'
    success_url = '/estoque/'

    def form_valid(self, form):
        # Get the current instance being updated
        instance = form.instance

        # Get the previous value from the database
        previous_quantidade = Estoque.objects.get(pk=instance.pk).quantidade

        # Compare the previous value with the updated value
        if form.cleaned_data['quantidade'] > previous_quantidade:
            return super().form_valid(form)
        else:
            form.add_error('quantidade', 'Nova quantidade não pode ser menor.')
            return self.form_invalid(form)
