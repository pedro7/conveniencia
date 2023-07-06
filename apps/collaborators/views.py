from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password, make_password
from django.http import HttpRequest
from django.shortcuts import redirect, render

from .forms import CollaboratorForm
from .models import Collaborator
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin


class CollaboratorListView(LoginRequiredMixin, ListView):
    model = Collaborator
    template_name = 'collaborators/collaborators.html'
    context_object_name = 'collaborators'


class CollaboratorCreateView(LoginRequiredMixin, CreateView):
    model = Collaborator
    form_class = CollaboratorForm
    template_name = 'collaborators/collaborators.html'
    success_url = '/colaboradores/'

@login_required
def cadastrar_colaborador(request: HttpRequest):
    form = CollaboratorForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect('visualizar_colaboradores')
    for error_list in form.errors.values():
        for error in error_list:
            messages.error(request, error)
    return redirect('visualizar_colaboradores')

@login_required
def visualizar_colaborador(request: HttpRequest, login):
    colaborador = Collaborator.objects.get(login=login)
    return render(request, 'collaborators/collaborator.html', {'colaborador': colaborador})
    
@login_required
def editar_colaborador(request: HttpRequest, login):
    colaborador = Collaborator.objects.get(login=login)
    copia = request.POST.copy()
    copia['senha'] = colaborador.password
    form = CollaboratorForm(copia, instance=colaborador)
    if form.is_valid():
        form.save()
        return redirect('visualizar_colaboradores')
    for error_list in form.errors.values():
        for error in error_list:
            messages.error(request, error)
    return render(request, 'colaboradores/colaborador.html', {'colaborador': colaborador})
    
def editar_senha(request: HttpRequest, login):
    colaborador = Collaborator.objects.get(login=login)
    if not check_password(request.POST['senha_atual'], colaborador.password):
        messages.error(request, 'Senha incorreta.')
        return render(request, 'colaboradores/colaborador.html', {'colaborador': colaborador})
    copia = request.POST.copy()
    copia['nome'] = colaborador.name
    copia['cpf'] = colaborador.cpf
    copia['login'] = colaborador.login
    copia['situacao'] = colaborador.status
    copia['senha'] = make_password(request.POST['senha_nova'])
    form = CollaboratorForm(copia, instance=colaborador)
    if form.is_valid():
        form.save()
        return redirect('visualizar_colaboradores')
    for error_list in form.errors.values():
        for error in error_list:
            messages.error(request, error)
    return render(request, 'colaboradores/colaborador.html', {'colaborador': colaborador})
    

@login_required
def alterar_situacao(request: HttpRequest, login):
    colaborador = Collaborator.objects.get(login=login)
    if colaborador.status == 'ativo':
        colaborador.status = 'inativo'
    else:
        colaborador.status = 'ativo'
    colaborador.save()
    return redirect('visualizar_colaboradores')
