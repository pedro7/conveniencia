from django.db import models
from django.forms import ModelForm
from barcodenumber import check_code_ean13
from django.core.exceptions import ValidationError


class Produto(models.Model):
    nome = models.CharField(max_length=50)
    codigo_barras = models.CharField(max_length=13, unique=True)
    preco = models.DecimalField(max_digits=4, decimal_places=2)

    def clean(self):
        self.clean_codigo_barras()

    def clean_codigo_barras(self):
        if not check_code_ean13(self.codigo_barras):
            raise ValidationError('Código de barras inválido.')


class ProdutoForm(ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'codigo_barras', 'preco']
