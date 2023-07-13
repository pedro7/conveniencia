from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import CreateView, ListView, UpdateView, View

from .models import Colaborador


class ColaboradorListView(LoginRequiredMixin, ListView):
    model = Colaborador
    template_name = 'colaboradores/colaboradores.html'
    context_object_name = 'colaboradores'


class ColaboradorCreateView(LoginRequiredMixin, CreateView):
    model = Colaborador
    fields = ['login', 'email', 'nome', 'cpf', 'senha']
    template_name = 'cadastrar.html'
    success_url = '/colaboradores/'

    def form_valid(self, form):
        form.instance.senha = make_password(form.cleaned_data['senha'])
        return super().form_valid(form)


class ColaboradorUpdateView(LoginRequiredMixin, UpdateView):
    model = Colaborador
    fields = ['login', 'email', 'nome']
    template_name = 'editar.html'
    success_url = '/colaboradores/'
    slug_field = 'login'
    slug_url_kwarg = 'login'


class ColaboradorUpdateSenhaView(LoginRequiredMixin, UpdateView):
    model = Colaborador
    fields = ['senha']
    template_name = 'editar.html'
    success_url = '/colaboradores/'
    slug_field = 'login'
    slug_url_kwarg = 'login'

    def form_valid(self, form):
        form.instance.senha = make_password(form.cleaned_data['senha'])
        return super().form_valid(form)


class ColaboradorUpdateSituacaoView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        colaborador = Colaborador.objects.get(login=kwargs['login'])
        if colaborador.situacao == 'ativo':
            colaborador.situacao = 'inativo'
        else:
            colaborador.situacao = 'ativo'
        colaborador.save()
        return redirect('visualizar_colaboradores')
