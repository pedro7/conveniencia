from django import forms


class AlterarQuantidadeForm(forms.Form):
    quantidade = forms.IntegerField()