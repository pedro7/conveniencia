from django.urls import path

from .views import PainelView, RedirecionarPainelView

urlpatterns = [
    path('', PainelView.as_view(), name='visualizar_painel'),
    path('painel/', RedirecionarPainelView.as_view())
]
