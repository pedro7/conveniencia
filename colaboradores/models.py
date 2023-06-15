from django.db import models


class Colaborador(models.Model):
    SITUACAO_CHOICES = [
        ('ativo', 'Ativo'),
        ('inativo', 'Inativo')
    ]
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=14)
    login = models.CharField(max_length=32)
    senha = models.CharField(max_length=128)
    situacao = models.CharField(max_length=7, choices=SITUACAO_CHOICES, default='ativo')
