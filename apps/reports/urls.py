from django.urls import path

from . import views

urlpatterns = [
    path('', views.visualizar_relatorios, name='visualizar_relatorios'),
    path('total-mensal/', views.gerar_total_mensal, name='gerar_total_mensal'),
    path('consumo-geral/', views.gerar_consumo_geral, name='gerar_consumo_geral')
]
