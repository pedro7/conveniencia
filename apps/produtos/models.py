from barcodenumber import check_code_ean13
from django.core.exceptions import ValidationError
from django.db import models


class Produto(models.Model):
    SITUACAO_CHOICES = [
        ('ativo', 'Ativo'),
        ('inativo', 'Inativo')
    ]
    nome = models.CharField(max_length=50)
    codigo_barras = models.CharField(max_length=13, unique=True)
    preco = models.DecimalField(max_digits=4, decimal_places=2)
    situacao = models.CharField(max_length=7, choices=SITUACAO_CHOICES, default='ativo')

    def clean(self):
        #self.clean_codigo_barras()
        pass

    def clean_codigo_barras(self):
        if not check_code_ean13(self.codigo_barras):
            raise ValidationError('Código de barras inválido.')
