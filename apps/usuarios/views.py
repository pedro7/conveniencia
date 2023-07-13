from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.views.generic import CreateView, ListView, UpdateView, View


class UsuarioListView(UserPassesTestMixin, ListView):
    model = User
    template_name = 'usuarios/usuarios.html'
    context_object_name = 'usuarios'

    def test_func(self):
        return self.request.user.is_superuser


class UsuarioCreateView(UserPassesTestMixin, CreateView):
    model = User
    fields = ['username', 'email', 'first_name', 'last_name', 'password']
    template_name = 'cadastrar.html'
    success_url = '/usuarios/'

    def test_func(self):
        return self.request.user.is_superuser
    
    def form_valid(self, form):
        form.instance.password = make_password(form.instance.password)
        return super().form_valid(form)


class UsuarioUpdateView(UserPassesTestMixin, UpdateView):
    model = User
    fields = ['username', 'email', 'first_name', 'last_name']
    template_name = 'editar.html'
    success_url = '/usuarios/'
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def test_func(self):
        return self.request.user.is_superuser
    

class UsuarioUpdateSenhaView(UserPassesTestMixin, UpdateView):
    model = User
    fields = ['password']
    template_name = 'editar.html'
    success_url = '/usuarios/'
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def test_func(self):
        return self.request.user.is_superuser
    
    def form_valid(self, form):
        form.instance.password = make_password(form.instance.password)
        return super().form_valid(form)


class UsuarioUpdateAdministradorView(UserPassesTestMixin, View):
    def get(self, request, *args, **kwargs):
        usuario = User.objects.get(username=kwargs['username'])
        usuario.is_superuser = not usuario.is_superuser
        usuario.save()
        return redirect('visualizar_usuarios')

    def test_func(self):
        return self.request.user.is_superuser

class UsuarioUpdateSituacaoView(UserPassesTestMixin, View):
    def get(self, request, *args, **kwargs):
        usuario = User.objects.get(username=kwargs['username'])
        usuario.is_active = not usuario.is_active
        usuario.save()
        return redirect('visualizar_usuarios')

    def test_func(self):
        return self.request.user.is_superuser
