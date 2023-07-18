from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import TemplateView, View

from util.relatorios import (get_relatorio_consumo_geral,
                             get_relatorio_total_mensal)


class GerarRelatorioTemplateView(UserPassesTestMixin, TemplateView):
    template_name = 'relatorios/relatorios.html'

    def test_func(self):
        return self.request.user.is_superuser
    

class GerarTotalMensalView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_superuser
    
    def get(self, request):
        return get_relatorio_total_mensal(request)


class GerarConsumoGeralView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_superuser
    
    def get(self, request):
        return get_relatorio_consumo_geral(request)
