from django.urls import path

from . import views

urlpatterns = [
    path('', views.colaboradores, name='colaboradores')
]
