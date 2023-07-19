from barcodenumber import check_code_ean13
from django.core.exceptions import ValidationError
from django.db import models


class Produto(models.Model):
    SITUACAO_CHOICES = [
        ('ativo', 'Ativo'),
        ('inativo', 'Inativo')
    ]
    TIPO_CHOICES = [
        ('normal', 'Normal'),
        ('alcoolico', 'Alcoólico'),
        ('ingresso', 'Ingresso'),
        ('vestimenta', 'Vestimenta')
    ]
    nome = models.CharField(max_length=50)
    codigo_barras = models.CharField(max_length=13, unique=True)
    preco = models.DecimalField(max_digits=4, decimal_places=2)
    situacao = models.CharField(max_length=7, choices=SITUACAO_CHOICES, default='ativo')
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES, default='normal')

    def clean(self):
        self.clean_codigo_barras()

    def clean_codigo_barras(self):
        if not check_code_ean13(self.codigo_barras):
            raise ValidationError('Código de barras inválido.')
