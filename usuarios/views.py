from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from django.db import IntegrityError


@login_required
def visualizar_usuarios(request: HttpRequest):
    if not request.user.is_superuser:
        return HttpResponse('Permissão insuficiente')
    usuarios = User.objects.all()
    return render(request, 'usuarios/usuarios.html', {'usuarios': usuarios})

@login_required
def cadastrar_usuario(request: HttpRequest):
    if not request.user.is_superuser:
        return HttpResponse('Permissão insuficiente')
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
def editar_usuario(request: HttpRequest, nome_usuario):
    if not request.user.is_superuser:
        return HttpResponse('Permissão insuficiente')
    usuario = User.objects.get(username=nome_usuario)
    if request.method == 'GET':
        return render(request, 'usuarios/editar-usuario.html', {'usuario': usuario})
    elif request.method == 'POST':
        usuario.username = request.POST['nome_usuario']
        usuario.email = request.POST['email']
        usuario.first_name = request.POST['nome']
        usuario.last_name = request.POST['sobrenome']
        usuario.password = make_password(request.POST['senha'])
        try:
            usuario.save()
        except IntegrityError:
            messages.error(request, 'Nome de usuário já existe.')
        return redirect('visualizar_usuarios')

@login_required
def excluir_usuario(request: HttpRequest, nome_usuario):
    if not request.user.is_superuser:
        return HttpResponse('Permissão insuficiente')
    User.objects.get(username=nome_usuario).delete()
    return redirect('visualizar_usuarios')
