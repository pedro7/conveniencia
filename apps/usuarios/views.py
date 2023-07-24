from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.views.generic import (CreateView, FormView, ListView, UpdateView,
                                  View)

from .forms import UserCreateForm, UsuarioSenhaForm


class UsuarioListView(UserPassesTestMixin, ListView):
    model = User
    template_name = 'usuarios/usuarios.html'
    context_object_name = 'usuarios'

    def test_func(self):
        return self.request.user.is_superuser


class UsuarioCreateView(UserPassesTestMixin, CreateView):
    model = User
    form_class = UserCreateForm
    template_name = 'base/cadastrar.html'
    success_url = '/usuarios/'

    def test_func(self):
        return self.request.user.is_superuser
    
    def form_valid(self, form):
        form.instance.password = make_password(form.instance.password)
        return super().form_valid(form)


class UsuarioUpdateView(UserPassesTestMixin, UpdateView):
    model = User
    fields = ['username', 'email', 'first_name', 'last_name']
    template_name = 'base/editar.html'
    success_url = '/usuarios/'
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def test_func(self):
        return self.request.user.is_superuser
    

class UsuarioUpdateSenhaView(UserPassesTestMixin, FormView):
    form_class = UsuarioSenhaForm
    template_name = 'base/editar.html'
    success_url = '/usuarios/'
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def test_func(self):
        return self.request.user.is_superuser
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        usuario = User.objects.get(username=self.kwargs['username'])
        kwargs['usuario'] = usuario
        return kwargs
    
    def form_valid(self, form):
        usuario = form.usuario
        nova_senha = form.cleaned_data['nova_senha']
        usuario.password = make_password(nova_senha)
        usuario.save()
        return super().form_valid(form)


class UsuarioUpdateAdministradorView(UserPassesTestMixin, View):
    def get(self, request, *args, **kwargs):
        usuario = User.objects.get(username=kwargs['username'])
        if usuario == request.user:
            messages.error(self.request, 'Não é possível remover permissões do seu próprio usuário.')
            return redirect('visualizar_usuarios')
        usuario.is_superuser = not usuario.is_superuser
        usuario.save()
        return redirect('visualizar_usuarios')

    def test_func(self):
        return self.request.user.is_superuser

class UsuarioUpdateSituacaoView(UserPassesTestMixin, View):
    def get(self, request, *args, **kwargs):
        usuario = User.objects.get(username=kwargs['username'])
        if usuario == request.user:
            messages.error(self.request, 'Não é possível inativar seu próprio usuário.')
            return redirect('visualizar_usuarios')
        usuario.is_active = not usuario.is_active
        usuario.save()
        return redirect('visualizar_usuarios')

    def test_func(self):
        return self.request.user.is_superuser
