from decimal import Decimal

from django.contrib.messages import error
from django.http.request import HttpRequest

from apps.produtos.models import Produto

from .compras import cadastrar_compra


def get_carrinho(request: HttpRequest):
    return request.session.get('carrinho', [])

def set_carrinho(request: HttpRequest, carrinho):
    request.session['carrinho'] = carrinho

def adicionar_no_carrinho(request: HttpRequest, id, nome, preco, tipo):
    carrinho = get_carrinho(request)
    produto = {
        'id': id,
        'nome': nome,
        'preco': str(preco),
        'tipo': tipo
    }
    carrinho.append(produto)
    set_carrinho(request, carrinho)

def remover_do_carrinho(request, posicao):
    carrinho = get_carrinho(request)
    carrinho.pop(posicao - 1)
    set_carrinho(request, carrinho)

def esvaziar_carrinho(request: HttpRequest):
    set_carrinho(request, [])

def get_total_carrinho(carrinho):
    total = 0
    for produto in carrinho:
        total += Decimal(produto['preco'])
    return total

def produto_pode_ser_adicionado(request, produto):
    quantidade = _get_quantidade_no_carrinho(request, produto)
    if produto.estoque.quantidade - quantidade < 0:
        error(request, 'Produto sem estoque.')
        return False
    else:
        return True

def _get_quantidade_no_carrinho(request, produto):
    quantidade = 1
    for produto_carrinho in get_carrinho(request):
        if produto.id == produto_carrinho['id']:
            quantidade += 1
    return quantidade

def finalizar_carrinho(request, colaborador):
    carrinho = get_carrinho(request)
    produtos = []
    for produto in carrinho:
        produtos.append(Produto.objects.get(id=int(produto['id'])))
    cadastrar_compra(colaborador, produtos)
