from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import TemplateView

from util.carrinho import *
from util.colaboradores import get_colaborador_valido
from util.compras import (get_gasto_referencia_atual_colaborador,
                          get_gasto_referencia_passada_colaborador)
from util.emails import (enviar_email_detalhes_refencias,
                         enviar_email_ultima_compra)
from util.produtos import get_produto_valido


class CarrinhoView(TemplateView):
    template_name = 'carrinho/carrinho.html'

    def get_context_data(self):
        context = super().get_context_data()
        carrinho = get_carrinho(self.request)
        context['carrinho'] = carrinho
        context['total'] = get_total_carrinho(carrinho)
        return context


class AdicionarProdutoView(View):
    def post(self, request: HttpRequest):
        produto = get_produto_valido(request, request.POST.get('codigo_barras'))
        if produto is None:
            return redirect('visualizar_carrinho')
        if not produto_pode_ser_adicionado(request, produto):
            return redirect('visualizar_carrinho')
        else:
            adicionar_no_carrinho(request, produto.pk, produto.nome, produto.preco, produto.tipo)
            return redirect('visualizar_carrinho')


class RemoverProdutoView(View):
    def post(self, request: HttpRequest, posicao):
        remover_do_carrinho(request, posicao)
        return redirect('visualizar_carrinho')


class EsvaziarCarrinhoView(View):
    def get(self, request):
        esvaziar_carrinho(request)
        return redirect('visualizar_carrinho')


class FinalizarCompraView(View):
    def post(self, request: HttpRequest):
        colaborador = get_colaborador_valido(request, request.POST['login'], request.POST['senha'])
        if not colaborador:
            return redirect('visualizar_carrinho')
        if not get_carrinho(request):
            enviar_email_detalhes_refencias(colaborador)
            return redirect('visualizar_carrinho')
        finalizar_carrinho(request, colaborador)
        enviar_email_ultima_compra(colaborador)
        esvaziar_carrinho(request)
        return redirect('visualizar_carrinho')


class ConsultarGastoMensalView(View):
    def post(self, request: HttpRequest):
        colaborador = get_colaborador_valido(request, request.POST['login'], request.POST['senha'])
        if not colaborador:
            return redirect('visualizar_carrinho')
        context = {
            'carrinho': get_carrinho(request),
            'gasto_mensal': get_gasto_referencia_atual_colaborador(colaborador),
            'gasto_referencia_passada': get_gasto_referencia_passada_colaborador(colaborador),
            'total': get_total_carrinho(get_carrinho(request))
        }
        enviar_email_detalhes_refencias(colaborador)
        return render(request, 'carrinho/carrinho.html', context)
