from django.views.generic import CreateView, DetailView, ListView, UpdateView

from .models import Colaborador


class ColaboradorListView(ListView):
    model = Colaborador
    template_name = 'colaboradores/colaboradores.html'
    context_object_name = 'colaboradores'


class ColaboradorCreateView(CreateView):
    model = Colaborador
    fields = ['login', 'email', 'nome', 'cpf', 'senha']
    template_name = 'colaboradores/cadastrar_colaborador.html'
    success_url = '/colaboradores/'


class ColaboradorDetailView(DetailView):
    model = Colaborador
    template_name = 'colaboradores/colaborador.html'
    context_object_name = 'colaborador'
    slug_field = 'login'
    slug_url_kwarg = 'login'


class ColaboradorUpdateView(UpdateView):
    model = Colaborador
    fields = ['login', 'email', 'nome']
    template_name = 'colaboradores/cadastrar_colaborador.html'
    success_url = '/colaboradores/'
    slug_field = 'login'
    slug_url_kwarg = 'login'
