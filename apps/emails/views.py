from django.core.mail import send_mail
from django.http import HttpRequest
from django.shortcuts import redirect, render


def visualizar_emails(request: HttpRequest):
    return render(request, 'emails/emails.html')

def enviar_email(request: HttpRequest):
    subject = request.POST['assunto']
    message = request.POST['mensagem']
    recipient_list = [request.POST['destinatario']]
    send_mail(subject, message, from_email=None, recipient_list=recipient_list)
    return redirect('visualizar_emails')
