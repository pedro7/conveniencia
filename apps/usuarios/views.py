from django.contrib.auth.models import User
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)


class UsuarioListView(ListView):
    model = User
    template_name = 'usuarios/usuarios.html'
    context_object_name = 'usuarios'


class UsuarioCreateView(CreateView):
    model = User
    fields = '__all__'
    template_name = 'usuarios/cadastrar_usuario.html'
    success_url = '/usuarios/'


class UsuarioDetailView(DetailView):
    model = User
    template_name = 'usuarios/usuario.html'
    context_object_name = 'usuario'
    slug_field = 'username'
    slug_url_kwarg = 'username'


class UsuarioUpdateView(UpdateView):
    model = User
    fields = '__all__'
    template_name = 'usuarios/cadastrar_usuario.html'
    success_url = '/usuarios/'
    slug_field = 'login'
    slug_url_kwarg = 'login'


class UsuarioDeleteView(DeleteView):
    model = User
    template_name = 'usuarios/cadastrar_usuario.html'
    success_url = 'usuarios'
