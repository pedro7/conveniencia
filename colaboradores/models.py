from django.core.exceptions import ValidationError
from django.db import models
from django.forms import ModelForm


class Colaborador(models.Model):
    SITUACAO_CHOICES = [
        ('ativo', 'Ativo'),
        ('inativo', 'Inativo')
    ]
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=11, unique=True)
    login = models.CharField(max_length=32, unique=True)
    senha = models.CharField(max_length=128)
    situacao = models.CharField(max_length=7, choices=SITUACAO_CHOICES, default='ativo')

    def clean(self):
        self.clean_cpf()

    def clean_cpf(self):
        # if not match(r'\d{3}\.\d{3}\.\d{3}-\d{2}', self.cpf):
        #     return False
        
        numbers = [int(digit) for digit in self.cpf if digit.isdigit()]

        if len(numbers) != 11 or len(set(numbers)) == 1:
            raise ValidationError('CPF inválido')

        sum_of_products = sum(a*b for a, b in zip(numbers[0:9], range(10, 1, -1)))
        expected_digit = (sum_of_products * 10 % 11) % 10
        if numbers[9] != expected_digit:
            raise ValidationError('CPF inválido')

        sum_of_products = sum(a*b for a, b in zip(numbers[0:10], range(11, 1, -1)))
        expected_digit = (sum_of_products * 10 % 11) % 10
        if numbers[10] != expected_digit:
            raise ValidationError('CPF inválido')
    

class ColaboradorForm(ModelForm):
    class Meta:
        model = Colaborador
        fields = ['nome', 'cpf', 'login', 'senha']