from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.http import HttpRequest
from django.shortcuts import redirect, render


@login_required
def visualizar_usuarios(request: HttpRequest):
    if not request.user.is_superuser:
        return redirect('entrar')
    usuarios = User.objects.all()
    return render(request, 'usuarios/usuarios.html', {'usuarios': usuarios})

@login_required
def cadastrar_usuario(request: HttpRequest):
    if not request.user.is_superuser:
        return redirect('entrar')
    nome_usuario = request.POST['nome_usuario']
    email = request.POST['email']
    nome = request.POST['nome']
    sobrenome = request.POST['sobrenome']
    senha = request.POST['senha']
    try:
        User.objects.create_user(nome_usuario, email, senha, first_name=nome, last_name=sobrenome)
    except IntegrityError:
        messages.error(request, 'Nome de usuário já existe.')
    return redirect('visualizar_usuarios')

@login_required
def visualizar_usuario(request: HttpRequest, username):
    if not request.user.is_superuser:
        return redirect('entrar')
    usuario = User.objects.get(username=username)
    return render(request, 'usuarios/usuario.html', {'usuario': usuario})

@login_required  
def editar_usuario(request: HttpRequest, nome_usuario):
    if not request.user.is_superuser:
        return redirect('entrar')
    usuario = User.objects.get(username=nome_usuario)
    usuario.username = request.POST['nome_usuario']
    usuario.email = request.POST['email']
    usuario.first_name = request.POST['nome']
    usuario.last_name = request.POST['sobrenome']
    try:
        usuario.save()
        return redirect('visualizar_usuarios')
    except IntegrityError:
        messages.error(request, 'Nome de usuário já existe.')
        return render(request, 'usuarios/usuario.html', {'usuario': usuario})

def editar_senha(request: HttpRequest, nome_usuario):
    if not request.user.is_superuser:
        return redirect('entrar')
    usuario = User.objects.get(username=nome_usuario)
    if not check_password(request.POST['senha_atual'], usuario.password):
        messages.error(request, 'Senha incorreta.')
        return render(request, 'usuarios/usuario.html', {'usuario': usuario})
    usuario.password = make_password(request.POST['senha_nova'])
    usuario.save()
    return redirect('visualizar_usuarios')

@login_required
def excluir_usuario(request: HttpRequest, nome_usuario):
    if not request.user.is_superuser:
        return redirect('entrar')
    User.objects.get(username=nome_usuario).delete()
    return redirect('visualizar_usuarios')
