from django.core.mail import EmailMessage

from .relatorios import get_relatorio_ultima_compra


def enviar_email_ultima_compra(colaborador):
    relatorio_ultima_compra = get_relatorio_ultima_compra().content
    email = EmailMessage(
        'Compra Lojinha SCI',
        to=[colaborador.email]
    )
    email.attach('Comprovante.pdf', relatorio_ultima_compra, 'application/pdf')
    email.send()
