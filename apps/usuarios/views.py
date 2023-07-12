from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import CreateView, ListView, UpdateView


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


class UsuarioUpdateView(UserPassesTestMixin, UpdateView):
    model = User
    fields = ['username', 'email', 'first_name', 'last_name']
    template_name = 'editar.html'
    success_url = '/usuarios/'
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def test_func(self):
        return self.request.user.is_superuser
