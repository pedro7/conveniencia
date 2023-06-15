from django.contrib.auth import authenticate, login
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def entrar(request: HttpRequest):
    if request.method == 'GET':
        return render(request, 'entrar.html')
    elif request.method == 'POST':
        nome_usuario = request.POST['nome_usuario']
        senha = request.POST['senha']
        usuario = authenticate(request, username=nome_usuario, password=senha)
        if usuario:
            login(request, usuario)
            return HttpResponse('logou')
        else:
            return HttpResponse('credenciais incorretas')


def sair(request: HttpRequest):
    pass
