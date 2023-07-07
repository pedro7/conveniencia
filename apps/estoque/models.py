from django.db import models

from apps.produtos.models import Produto


class Estoque(models.Model):
    produto = models.OneToOneField(Produto, models.CASCADE)
    quantidade = models.IntegerField(default=0)
