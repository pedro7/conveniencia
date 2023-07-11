from django.contrib import messages
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import TemplateView

from apps.produtos.models import Produto
from util.carrinho import (add_to_carrinho, criar_carrinho, esvaziar_carrinho,
                           finalizar_compra, get_carrinho, get_total_carrinho)
from util.colaboradores import get_colaborador_valido
from util.compras import (get_gasto_referencia_atual_colaborador,
                          get_gasto_referencia_passada_colaborador)
from util.emails import enviar_email_ultima_compra


class CarrinhoView(TemplateView):
    template_name = 'carrinho/carrinho.html'

    def get_context_data(self):
        context = super().get_context_data()
        carrinho = criar_carrinho(self.request)
        context['carrinho'] = carrinho
        context['total'] = get_total_carrinho(carrinho)
        return context


class AdicionarProdutoView(View):
    def post(self, request: HttpRequest):
        codigo_barras = request.POST.get('codigo_barras')
        produto = get_object_or_404(Produto, codigo_barras=codigo_barras)
        if produto.situacao == 'inativo':
            messages.error(request, 'Produto inativo')
            return redirect('visualizar_carrinho')
        
        qtd_estoque = produto.estoque.quantidade
        for produto_carrinho in get_carrinho:
            if str(produto.pk) == str(produto_carrinho['id']):
                qtd_estoque -= 1
        if qtd_estoque <= 0:
            messages.error(request, 'Produto sem estoque.')
            return redirect('visualizar_carrinho')
        
        add_to_carrinho(request, produto.pk, produto.nome, produto.preco, produto.tipo)
        return redirect('visualizar_carrinho')


class RemoverProdutoView(View):
    def post(self, request: HttpRequest, posicao):
        carrinho = request.session.get('carrinho', [])
        if posicao >= 1 and posicao <= len(carrinho):
            carrinho.pop(posicao - 1)
            request.session['carrinho'] = carrinho
        return redirect('visualizar_carrinho')


class EsvaziarCarrinhoView(View):
    def post(self, request):
        esvaziar_carrinho(request)
        return redirect('visualizar_carrinho')


class FinalizarCompraView(View):
    def post(self, request: HttpRequest):
        colaborador = get_colaborador_valido(request, request.POST['login'], request.POST['senha'])
        if not colaborador:
            return redirect('visualizar_carrinho')
        finalizar_compra(request, colaborador)
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
            'gasto_referencia_passada': get_gasto_referencia_passada_colaborador(colaborador)
        }
        return render(request, 'carrinho/carrinho.html', context)
