from django.urls import path

from . import views

urlpatterns = [
    path('', views.visualizar_emails, name='visualizar_emails'),
    path('enviar/', views.enviar_email, name='enviar_email')
]