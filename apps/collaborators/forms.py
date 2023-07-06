from django import forms

from .models import Collaborator


class CollaboratorForm(forms.ModelForm):
    class Meta:
        model = Collaborator
        fields = ['name', 'cpf', 'login', 'password']
