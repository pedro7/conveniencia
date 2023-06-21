from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.contrib import messages


@login_required
def usuarios(request: HttpRequest):
    if request.user.is_superuser:
        usuarios = User.objects.all()
        return render(request, 'usuarios/usuarios.html', {'usuarios': usuarios})
    else:
        return HttpResponse('permissão insufciente')

def entrar(request: HttpRequest):
    if request.method == 'GET':
        return render(request, 'usuarios/entrar.html')
    elif request.method == 'POST':
        nome_usuario = request.POST['nome_usuario']
        senha = request.POST['senha']
        usuario = authenticate(request, username=nome_usuario, password=senha)
        if usuario:
            login(request, usuario)
            return redirect('painel')
        else:
            messages.error(request, 'Credenciais incorretas')
            return redirect('entrar')

def sair(request: HttpRequest):
    if request.method == 'GET':
        logout(request)
        return redirect('entrar')

def cadastrar_usuario(request: HttpRequest):
    if request.user.is_superuser:
        nome_usuario = request.POST['nome_usuario']
        email = request.POST['email']
        nome = request.POST['nome']
        sobrenome = request.POST['sobrenome']
        senha = request.POST['senha']
        User.objects.create_user(nome_usuario, email, senha, first_name=nome, last_name=sobrenome)
        return redirect('usuarios')
    
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
            return redirect('usuarios')

def excluir_usuario(request: HttpRequest, nome_usuario):
    if request.user.is_superuser:
        User.objects.get(username=nome_usuario).delete()
        return redirect('usuarios')
