from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.http import HttpRequest
from django.shortcuts import redirect, render

from .models import Colaborador, ColaboradorForm


@login_required
def visualizar_colaboradores(request: HttpRequest):
    if request.method == 'GET':
        colaboradores = Colaborador.objects.all()
        return render(request, 'colaboradores/colaboradores.html', {'colaboradores': colaboradores})

@login_required
def cadastrar_colaborador(request: HttpRequest):
    if request.method == 'POST':
        request.POST = request.POST.copy()
        request.POST['senha'] = make_password(request.POST['senha'])
        form = ColaboradorForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            for error_list in form.errors.values():
                for error in error_list:
                    messages.error(request, error)
        return redirect('visualizar_colaboradores')
    
@login_required
def editar_colaborador(request: HttpRequest, login):
    colaborador = Colaborador.objects.get(login=login)
    if request.method == 'GET':
        return render(request, 'colaboradores/editar-colaborador.html', {'colaborador': colaborador})
    elif request.method == 'POST':
        form = ColaboradorForm(request.POST, instance=colaborador)
        if form.is_valid():
            form.save()
        else:
            for error_list in form.errors.values():
                for error in error_list:
                    messages.error(request, error)
            return render(request, 'colaboradores/editar-colaborador.html', {'colaborador': colaborador})
        return redirect('visualizar_colaboradores')
    
@login_required
def ativar_colaborador(request: HttpRequest, login):
    if request.method == 'POST':
        colaborador = Colaborador.objects.get(login=login)
        colaborador.situacao = 'ativo'
        colaborador.save()
        return redirect('visualizar_colaboradores')

@login_required
def inativar_colaborador(request: HttpRequest, login):
    if request.method == 'POST':
        colaborador = Colaborador.objects.get(login=login)
        colaborador.situacao = 'inativo'
        colaborador.save()
        return redirect('visualizar_colaboradores')
