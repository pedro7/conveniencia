from django import forms
from django.core.validators import MaxLengthValidator

from .models import Produto


class ProdutoForm(forms.ModelForm):
    codigo_barras = forms.CharField(label='Código de Barras', validators=[MaxLengthValidator(15)])
    preco = forms.CharField(label='Preço', validators=[MaxLengthValidator(10)])
    
    class Meta:
        model = Produto
        fields = ['nome', 'codigo_barras', 'preco', 'tipo']
        labels = {
            'nome': 'Nome',
            'tipo': 'Tipo',
        }
