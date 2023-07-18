from django.contrib import messages
from django.contrib.auth.hashers import check_password

from apps.colaboradores.models import Colaborador
from apps.compras.models import Compra
from util.referencias import get_referencia_passada


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

def get_colaboradores_compraram_produto_desde_referencia_passada(produto):
    compras = []
    for compra in Compra.objects.filter(data__gte=get_referencia_passada()):
        for compra_produto in compra.compra_produtos.all():
            if compra_produto.produto == produto:
                compras.append(compra)
    colaboradores = []
    for compra in compras:
        if not compra.colaborador.email in colaboradores:
            colaboradores.append(compra.colaborador.email)
    return colaboradores
