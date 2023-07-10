from django.urls import path

from .views import EstoqueListView, EstoqueUpdateView

urlpatterns = [
    path('', EstoqueListView.as_view(), name='visualizar_estoque'),
    path('<int:pk>/editar/', EstoqueUpdateView.as_view(), name='editar_estoque')
]
