from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password, make_password
from django.http import HttpRequest
from django.shortcuts import redirect, render

from .forms import ColaboradorForm
from .models import Colaborador


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
def visualizar_colaborador(request: HttpRequest, login):
    colaborador = Colaborador.objects.get(login=login)
    return render(request, 'colaboradores/colaborador.html', {'colaborador': colaborador})
    
@login_required
def editar_colaborador(request: HttpRequest, login):
    colaborador = Colaborador.objects.get(login=login)
    copia = request.POST.copy()
    copia['senha'] = colaborador.senha
    form = ColaboradorForm(copia, instance=colaborador)
    if form.is_valid():
        form.save()
        return redirect('visualizar_colaboradores')
    for error_list in form.errors.values():
        for error in error_list:
            messages.error(request, error)
    return render(request, 'colaboradores/colaborador.html', {'colaborador': colaborador})
    
def editar_senha(request: HttpRequest, login):
    colaborador = Colaborador.objects.get(login=login)
    if not check_password(request.POST['senha_atual'], colaborador.senha):
        messages.error(request, 'Senha incorreta.')
        return render(request, 'colaboradores/colaborador.html', {'colaborador': colaborador})
    copia = request.POST.copy()
    copia['nome'] = colaborador.nome
    copia['cpf'] = colaborador.cpf
    copia['login'] = colaborador.login
    copia['situacao'] = colaborador.situacao
    copia['senha'] = make_password(request.POST['senha_nova'])
    form = ColaboradorForm(copia, instance=colaborador)
    if form.is_valid():
        form.save()
        return redirect('visualizar_colaboradores')
    for error_list in form.errors.values():
        for error in error_list:
            messages.error(request, error)
    return render(request, 'colaboradores/colaborador.html', {'colaborador': colaborador})
    

@login_required
def alterar_situacao(request: HttpRequest, login):
    colaborador = Colaborador.objects.get(login=login)
    if colaborador.situacao == 'ativo':
        colaborador.situacao = 'inativo'
    else:
        colaborador.situacao = 'ativo'
    colaborador.save()
    return redirect('visualizar_colaboradores')
