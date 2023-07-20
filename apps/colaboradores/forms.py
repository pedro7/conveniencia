from django import forms
from django.contrib.auth.hashers import check_password
from django.core.validators import MaxLengthValidator

from .models import Colaborador


class ColaboradorCreateForm(forms.ModelForm):
    cpf = forms.CharField(label='CPF', validators=[MaxLengthValidator(14)])
    
    class Meta:
        model = Colaborador
        fields = ['login', 'email', 'nome', 'cpf', 'data_de_nascimento', 'senha']
        labels = {
            'login': 'Login',
            'email': 'Email',
            'nome': 'Nome',
            'data_de_nascimento': 'Data de Nascimento',
        }


class ColaboradorUpdateForm(forms.ModelForm):
    cpf = forms.CharField(validators=[MaxLengthValidator(14)])
    
    class Meta:
        model = Colaborador
        fields = ['login', 'email', 'nome', 'cpf', 'data_de_nascimento']
        labels = {
            'login': 'Login',
            'email': 'Email',
            'nome': 'Nome',
            'cpf': 'CPF',
            'data_de_nascimento': 'Data de Nascimento',
        }


class ColaboradorUpdateSenhaForm(forms.Form):
    senha_atual = forms.CharField(max_length=255, widget=forms.PasswordInput)
    nova_senha = forms.CharField(max_length=255, widget=forms.PasswordInput)
    confirmar_nova_senha = forms.CharField(max_length=255, widget=forms.PasswordInput)

    def __init__(self, colaborador, *args, **kwargs):
        self.colaborador = colaborador
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        senha_atual = cleaned_data.get('senha_atual')
        nova_senha = cleaned_data.get('nova_senha')
        confirmar_nova_senha = cleaned_data.get('confirmar_nova_senha')

        if senha_atual and not check_password(senha_atual, self.colaborador.senha):
            self.add_error('senha_atual', 'A senha atual está incorreta.')

        if nova_senha != confirmar_nova_senha:
            self.add_error('confirmar_nova_senha', 'As senhas não correspondem.')

        return cleaned_data
