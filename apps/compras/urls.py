from django.urls import path

from .views import CompraDeleteView, CompraDetailView, CompraListView

urlpatterns = [
    path('', CompraListView.as_view(), name='visualizar_compras'),
    path('<int:pk>/', CompraDetailView.as_view(), name='visualizar_compra_produtos'),
    path('<int:pk>/excluir/', CompraDeleteView.as_view(), name='excluir_compra')
]
