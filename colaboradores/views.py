from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.http import HttpRequest
from django.shortcuts import redirect, render

from .models import Colaborador, ColaboradorForm


@login_required
def visualizar_colaboradores(request: HttpRequest):
    colaboradores = Colaborador.objects.all()
    return render(request, 'colaboradores/colaboradores.html', {'colaboradores': colaboradores})

@login_required
def cadastrar_colaborador(request: HttpRequest):
    copia = request.POST.copy()
    copia['senha'] = make_password(copia['senha'])
    form = ColaboradorForm(copia)
    if form.is_valid():
        form.save()
        return redirect('visualizar_colaboradores')
    for error_list in form.errors.values():
        for error in error_list:
            messages.error(request, error)
    return redirect('visualizar_colaboradores')
    
@login_required
def editar_colaborador(request: HttpRequest, login):
    colaborador = Colaborador.objects.get(login=login)
    if request.method == 'GET':
        return render(request, 'colaboradores/editar-colaborador.html', {'colaborador': colaborador})
    copia = request.POST.copy()
    copia['senha'] = make_password(copia['senha'])
    form = ColaboradorForm(copia, instance=colaborador)
    if form.is_valid():
        form.save()
        return redirect('visualizar_colaboradores')
    for error_list in form.errors.values():
        for error in error_list:
            messages.error(request, error)
    return render(request, 'colaboradores/editar-colaborador.html', {'colaborador': colaborador})
    
@login_required
def alterar_situacao(request: HttpRequest, login):
    colaborador = Colaborador.objects.get(login=login)
    if colaborador.situacao == 'ativo':
        colaborador.situacao = 'inativo'
    else:
        colaborador.situacao = 'ativo'
    colaborador.save()
    return redirect('visualizar_colaboradores')
