from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render


def entrar(request: HttpRequest):
    if request.method == 'GET':
        return render(request, 'autenticacao/entrar.html')
    elif request.method == 'POST':
        nome_usuario = request.POST['nome_usuario']
        senha = request.POST['senha']
        usuario = authenticate(request, username=nome_usuario, password=senha)
        if usuario:
            login(request, usuario)
            return redirect('visualizar_painel')
        else:
            messages.error(request, 'Credenciais incorretas')
            return redirect('entrar')

def sair(request: HttpRequest):
    if request.user:
        logout(request)
    return redirect('entrar')