from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render


@login_required
def visualizar_usuarios(request: HttpRequest):
    if request.user.is_superuser:
        usuarios = User.objects.all()
        return render(request, 'usuarios/usuarios.html', {'usuarios': usuarios})
    else:
        return HttpResponse('permissão insufciente')

@login_required
def cadastrar_usuario(request: HttpRequest):
    if request.user.is_superuser:
        nome_usuario = request.POST['nome_usuario']
        email = request.POST['email']
        nome = request.POST['nome']
        sobrenome = request.POST['sobrenome']
        senha = request.POST['senha']
        User.objects.create_user(nome_usuario, email, senha, first_name=nome, last_name=sobrenome)
        return redirect('visualizar_usuarios')

@login_required  
def editar_usuario(request: HttpRequest, nome_usuario):
    if request.user.is_superuser:
        usuario = User.objects.get(username=nome_usuario)
        if request.method == 'GET':
            return render(request, 'usuarios/editar-usuario.html', {'usuario': usuario})
        elif request.method == 'POST':
            usuario.username = request.POST['nome_usuario']
            usuario.email = request.POST['email']
            usuario.first_name = request.POST['nome']
            usuario.last_name = request.POST['sobrenome']
            usuario.password = make_password(request.POST['senha'])
            usuario.save()
            return redirect('visualizar_usuarios')

@login_required
def excluir_usuario(request: HttpRequest, nome_usuario):
    if request.user.is_superuser:
        User.objects.get(username=nome_usuario).delete()
        return redirect('visualizar_usuarios')
