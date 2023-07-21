from django.core.mail import send_mail
from django.http import HttpRequest
from django.shortcuts import redirect, render

from apps.colaboradores.models import Colaborador


def visualizar_emails(request: HttpRequest):
    colaboradores = Colaborador.objects.all()
    return render(request, 'emails/emails.html', {'colaboradores': colaboradores})

def enviar_email(request: HttpRequest):
    subject = request.POST['assunto']
    message = request.POST['mensagem']
    recipient_list = [request.POST['destinatario']]
    send_mail(subject, message, from_email=None, recipient_list=recipient_list)
    return redirect('visualizar_emails')
