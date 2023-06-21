from django.urls import path

from . import views

urlpatterns = [
    path('', views.visualizar_painel, name='visualizar_painel')
]
