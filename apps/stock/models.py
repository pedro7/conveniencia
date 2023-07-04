from django.db import models

from apps.produtos.models import Produto


class Stock(models.Model):
    product = models.OneToOneField(Produto, models.CASCADE)
