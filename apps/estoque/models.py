from django.db import models

from apps.produtos.models import Produto
from django.contrib.auth.models import User


class Estoque(models.Model):
    produto = models.OneToOneField(Produto, models.CASCADE)
    quantidade = models.IntegerField(default=0)
