from django.db import models


class Colaborador(models.Model):
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=14)
    #login
    #senha
    #situacao
