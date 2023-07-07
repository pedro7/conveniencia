from django.urls import path

from .views import CompraDeleteView, ComprasListView

urlpatterns = [
    path('', ComprasListView.as_view(), name='visualizar_compras'),
    path('excluir/<int:pk>/', CompraDeleteView.as_view(), name='excluir_compra')
]
