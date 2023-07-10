from collections import Counter
from decimal import Decimal
from apps.compras.models import Compra
from apps.produtos.models import Produto
from util.emails import enviar_email_compra_ingresso, enviar_email_compra_roupa


def finalizar_compra(request, colaborador):
    carrinho = request.session.get('carrinho', [])
    compra = Compra.objects.create(colaborador=colaborador)
    lista = []
    for produto in carrinho:
        if produto['tipo'] == 'ingresso':
            enviar_email_compra_ingresso(colaborador)
        if produto['tipo'] == 'roupa':
            enviar_email_compra_roupa(colaborador)
        lista.append(produto['id'])
    counter = Counter(lista)
    for produto, quantidade in counter.items():
        produto2 = Produto.objects.get(id=int(produto))
        estoque = produto2.estoque
        estoque.quantidade -= int(quantidade)
        estoque.save()
        through_defaults = {
            'quantidade': quantidade,
            'preco_unitario': produto2.preco
        }
        compra.produtos.add(produto, through_defaults=through_defaults)

def get_total_carrinho(carrinho):
    total = 0
    for produto in carrinho:
        total += Decimal(produto['preco'])
    return total