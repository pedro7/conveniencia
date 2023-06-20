from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from .models import Colaborador


@login_required
def colaboradores(request: HttpRequest):
    if request.method == 'GET':
        colaboradores = Colaborador.objects.all()
        return render(request, 'colaboradores/colaboradores.html', {'colaboradores': colaboradores})

@login_required
def cadastrar_colaborador(request: HttpRequest):
    if request.method == 'POST':
        nome = request.POST['nome']
        cpf = request.POST['cpf']
        login = request.POST['login']
        senha = request.POST['senha']
        Colaborador.objects.create(nome=nome, cpf=cpf, login=login, senha=senha)
        return redirect('colaboradores')
    
@login_required
def editar_colaborador(request: HttpRequest, login):
    colaborador = Colaborador.objects.get(login=login)
    if request.method == 'GET':
        return render(request, 'colaboradores/editar-colaborador.html', {'colaborador': colaborador})
    elif request.method == 'POST':
        colaborador.nome = request.POST['nome']
        colaborador.cpf = request.POST['cpf']
        colaborador.login = request.POST['login']
        colaborador.senha = request.POST['senha']
        colaborador.save()
        return redirect('colaboradores')
    
@login_required
def ativar_colaborador(request: HttpRequest, login):
    if request.method == 'POST':
        colaborador = Colaborador.objects.get(login=login)
        colaborador.situacao = 'ativo'
        colaborador.save()
        return redirect('colaboradores')

@login_required
def inativar_colaborador(request: HttpRequest, login):
    if request.method == 'POST':
        colaborador = Colaborador.objects.get(login=login)
        colaborador.situacao = 'inativo'
        colaborador.save()
        return redirect('colaboradores')
