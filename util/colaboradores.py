from django.contrib import messages
from django.contrib.auth.hashers import check_password

from apps.colaboradores.models import Colaborador


def get_colaborador_valido(request, login, senha):
    try:
        colaborador = Colaborador.objects.get(login=login)
    except Colaborador.DoesNotExist:
        messages.error(request, 'Colaborador não cadastrado.')
        return None
    if colaborador.situacao == 'inativo':
        messages.error(request, 'Colaborador inativo.')
        return None
    if not check_password(senha, colaborador.senha):
        messages.error(request, 'Senha incorreta.')
        return None
    return colaborador