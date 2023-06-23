from django.urls import path

from . import views

urlpatterns = [
    path('', views.visualizar_relatorios, name='visualizar_relatorios'),
]
