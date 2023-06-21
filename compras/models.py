from django.db import models
from colaboradores.models import Colaborador
from produtos.models import Produto


class Compra(models.Model):
    colaborador = models.ForeignKey(Colaborador, on_delete=models.PROTECT)
    produtos = models.ManyToManyField(Produto, through='CompraProduto')
    data = models.DateTimeField(auto_now_add=True)


class CompraProduto(models.Model):
    compra = models.ForeignKey(Compra, on_delete=models.PROTECT)
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT)
    quantidade = models.IntegerField()
