from apps.produtos.models import Produto

def diminuir_estoque(produto: Produto, quantidade):
    produto.estoque.quantidade -= quantidade
    produto.save()