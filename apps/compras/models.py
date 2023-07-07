from django.db import models
from apps.colaboradores.models import Colaborador
from apps.produtos.models import Produto


class Compra(models.Model):
    colaborador = models.ForeignKey(Colaborador, on_delete=models.PROTECT)
    produtos = models.ManyToManyField(Produto, through='CompraProduto')
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        compraprodutos = self.compra_produtos.all()
        produtos_info = ", ".join([f"{cp.produto} ({cp.quantidade})" for cp in compraprodutos])
        return f"Compra ID: {self.id}, Colaborador: {self.colaborador}, Produtos: {produtos_info}, Data: {self.data}"


class CompraProduto(models.Model):
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE, related_name='compra_produtos')
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT)
    quantidade = models.IntegerField()
    preco_unitario = models.DecimalField(max_digits=4, decimal_places=2)
