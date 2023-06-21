from django.urls import path

from . import views

urlpatterns = [
    path('', views.visualizar_compras, name='visualizar_compras'),
    path('excluir/<int:id>/', views.excluir_compra, name='excluir_compra')
]
