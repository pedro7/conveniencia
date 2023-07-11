from django.contrib.auth.models import User
from django.db import models

from apps.produtos.models import Produto


class Movimentacao(models.Model):
    TIPO_CHOICES = [
        ('entrada', 'Entrada'),
        ('saida', 'Saída')
    ]
    produto = models.ForeignKey(Produto, models.PROTECT)
    usuario = models.ForeignKey(User, models.PROTECT)
    quantidade = models.IntegerField()
    data = models.DateTimeField(auto_now_add=True)
    tipo = models.CharField(max_length=7, choices=TIPO_CHOICES)