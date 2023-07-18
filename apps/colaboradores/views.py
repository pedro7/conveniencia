from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import (CreateView, FormView, ListView, UpdateView,
                                  View)

from .forms import ColaboradorSenhaForm
from .models import Colaborador


class ColaboradorListView(LoginRequiredMixin, ListView):
    model = Colaborador
    template_name = 'colaboradores/colaboradores.html'
    context_object_name = 'colaboradores'


class ColaboradorCreateView(LoginRequiredMixin, CreateView):
    model = Colaborador
    fields = ['login', 'email', 'nome', 'cpf', 'senha']
    template_name = 'base/cadastrar.html'
    success_url = '/colaboradores/'

    def form_valid(self, form):
        form.instance.senha = make_password(form.cleaned_data['senha'])
        return super().form_valid(form)


class ColaboradorUpdateView(LoginRequiredMixin, UpdateView):
    model = Colaborador
    fields = ['login', 'email', 'nome', 'cpf']
    template_name = 'base/editar.html'
    success_url = '/colaboradores/'
    slug_field = 'login'
    slug_url_kwarg = 'login'

    def form_valid(self, form):
        form.instance.senha = make_password(form.cleaned_data['senha'])
        return super().form_valid(form)


class ColaboradorUpdateSenhaView(LoginRequiredMixin, FormView):
    form_class = ColaboradorSenhaForm
    template_name = 'base/editar.html'
    success_url = '/colaboradores/'
    slug_field = 'login'
    slug_url_kwarg = 'login'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        colaborador = Colaborador.objects.get(login=self.kwargs['login'])
        kwargs['colaborador'] = colaborador
        return kwargs
    
    def form_valid(self, form):
        colaborador = form.colaborador
        nova_senha = form.cleaned_data['nova_senha']
        colaborador.senha = make_password(nova_senha)
        colaborador.save()
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
