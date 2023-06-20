from django.db import models


class Produto(models.Model):
    nome = models.CharField(max_length=50)
    codigo_barras = models.CharField(max_length=13)
    preco = models.DecimalField(max_digits=4, decimal_places=2)
