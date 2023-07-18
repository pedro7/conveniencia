from django.core.mail import EmailMessage

from apps.produtos.models import Produto

from .relatorios import get_relatorio_ultima_compra, get_relatorio_mudanca_preco_produto, get_relatorio_consumo_colaborador
from .colaboradores import get_colaboradores_compraram_produto_desde_referencia_passada


def enviar_email_ultima_compra(colaborador):
    relatorio_ultima_compra = get_relatorio_ultima_compra().content
    email = EmailMessage(
        'Compra Conveniência SCI',
        to=[colaborador.email]
    )
    email.attach('Comprovante.pdf', relatorio_ultima_compra, 'application/pdf')
    email.send()

def enviar_email_compra_ingresso(colaborador, quantidade):
    email = EmailMessage(
        'Compra Ingresso SCI',
        to=[colaborador.email, 'pedrogabrielappel@gmail.com']
    )
    email.send()

def enviar_email_compra_roupa(colaborador, quantidade):
    email = EmailMessage(
        'Compra Roupa SCI',
        to=[colaborador.email, 'pedrogabrielappel@gmail.com']
    )
    email.send()

def enviar_email_mudanca_preco_produto(pk, preco_novo, preco_antigo):
    produto = Produto.objects.get(pk=pk)
    colaboradores = get_colaboradores_compraram_produto_desde_referencia_passada(produto)
    relatorio = get_relatorio_mudanca_preco_produto(produto, preco_novo, preco_antigo).content
    if colaboradores:
        for colaborador in colaboradores:
            email = EmailMessage(
                'Alteração no preço do produto',
                f'Você está recebendo esse email pois houve alteração no preço de um produto que você comprou recentemente.',
                to=[colaborador]
            )
            email.attach('Alteração de preço.pdf', relatorio, 'application/pdf')
            email.send()

def enviar_email_detalhes_refencias(colaborador):
    relatorio = get_relatorio_consumo_colaborador(colaborador).content
    email = EmailMessage(
        'Detalhes referência atual e passada',
        f'Você está recebendo esse email pois passou o crachá na Conveniência SCI sem nenhum item no carrinho.',
        to=[colaborador.email]
    )
    email.attach('Alteração de preço.pdf', relatorio, 'application/pdf')
    email.send()
