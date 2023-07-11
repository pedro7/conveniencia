from django.contrib.auth.models import User
from django.views.generic import CreateView, DeleteView, ListView, UpdateView


class UsuarioListView(ListView):
    model = User
    template_name = 'usuarios/usuarios.html'
    context_object_name = 'usuarios'


class UsuarioCreateView(CreateView):
    model = User
    fields = ['username', 'email', 'first_name', 'last_name', 'password']
    template_name = 'cadastrar.html'
    success_url = '/usuarios/'


class UsuarioUpdateView(UpdateView):
    model = User
    fields = ['username', 'email', 'first_name', 'last_name']
    template_name = 'editar.html'
    success_url = '/usuarios/'
    slug_field = 'username'
    slug_url_kwarg = 'username'


class UsuarioDeleteView(DeleteView):
    model = User
    template_name = 'usuarios/cadastrar_usuario.html'
    success_url = 'usuarios'
