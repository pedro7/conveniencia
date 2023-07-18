from django.urls import path

from .views import (GerarConsumoGeralView, GerarTotalMensalView,
                    GerarRelatorioTemplateView)

urlpatterns = [
    path('gerar/', GerarRelatorioTemplateView.as_view(), name='gerar_relatorios'),
    path('gerar/total-mensal/', GerarTotalMensalView.as_view(), name='gerar_total_mensal'),
    path('gerar/consumo-geral/', GerarConsumoGeralView.as_view(), name='gerar_consumo_geral')
]
