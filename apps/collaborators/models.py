from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.db import models


class Collaborator(models.Model):
    STATUS_CHOICES = [
        ('ativo', 'Ativo'),
        ('inativo', 'Inativo')
    ]
    name = models.CharField(max_length=100)
    cpf = models.CharField(max_length=11, unique=True)
    login = models.CharField(max_length=32, unique=True)
    password = models.CharField(max_length=255)
    status = models.CharField(max_length=7, choices=STATUS_CHOICES, default='ativo')

    def save(self, *args, **kwargs):
        self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def clean(self):
        #self.clean_cpf()
        pass

    def clean_cpf(self):
        # if not match(r'\d{3}\.\d{3}\.\d{3}-\d{2}', self.cpf):
        #     return False
        
        numbers = [int(digit) for digit in self.cpf if digit.isdigit()]

        if len(numbers) != 11 or len(set(numbers)) == 1:
            raise ValidationError('Cpf inválido.')

        sum_of_products = sum(a*b for a, b in zip(numbers[0:9], range(10, 1, -1)))
        expected_digit = (sum_of_products * 10 % 11) % 10
        if numbers[9] != expected_digit:
            raise ValidationError('Cpf inválido.')

        sum_of_products = sum(a*b for a, b in zip(numbers[0:10], range(11, 1, -1)))
        expected_digit = (sum_of_products * 10 % 11) % 10
        if numbers[10] != expected_digit:
            raise ValidationError('Cpf inválido.')
