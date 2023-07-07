from collections import Counter

from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import TemplateView

from apps.colaboradores.models import Colaborador
from apps.compras.models import Compra
from apps.produtos.models import Produto
from util.emails import enviar_email_ultima_compra
from util.vendas import get_referencia_atual, get_referencia_passada


class CarrinhoView(TemplateView):
    template_name = 'carrinho/carrinho.html'

    def get_context_data(self):
        context = super().get_context_data()
        carrinho = self.request.session.get('carrinho', [])
        total = sum(float(produto['preco']) for produto in carrinho)
        context['carrinho'] = carrinho
        context['total'] = total
        return context


class AdicionarProdutoView(View):
    def post(self, request: HttpRequest):
        codigo_barras = request.POST.get('codigo_barras')
        produto = get_object_or_404(Produto, codigo_barras=codigo_barras)
        
        carrinho = request.session.get('carrinho', [])
        produto_data = {
            'id': produto.pk,
            'preco': str(produto.preco),
        }
        carrinho.append(produto_data)
        request.session['carrinho'] = carrinho
        
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
        request.session['carrinho'] = []
        return redirect('visualizar_carrinho')


class FinalizarCompraView(View):
    def post(self, request: HttpRequest):
        colaborador = _get_colaborador_valido(request, request.POST['login'], request.POST['senha'])
        if not colaborador:
            return redirect('visualizar_carrinho')
        
        carrinho = request.session.get('carrinho', [])
        compra = Compra.objects.create(colaborador=colaborador)
        lista = []
        for produto in carrinho:
            lista.append(produto['id'])
        counter = Counter(lista)
        for produto, quantidade in counter.items():
            print(produto, quantidade)
            through_defaults = {
                'quantidade': quantidade,
                'preco_unitario': Produto.objects.get(id=produto).preco
            }
            compra.produtos.add(produto, through_defaults=through_defaults)
        enviar_email_ultima_compra(colaborador)
        request.session['carrinho'] = []
        return redirect('visualizar_carrinho')


class ConsultarGastoMensalView(View):
    def post(self, request: HttpRequest):
        colaborador = _get_colaborador_valido(request, request.POST['login'], request.POST['senha'])
        if not colaborador:
            return redirect('visualizar_carrinho')
        gasto_referencia_atual = 0
        referencia_atual = get_referencia_atual()
        for compra in Compra.objects.filter(colaborador=colaborador, data__gte=referencia_atual):
            for compra_produto in compra.compra_produtos.all():
                gasto_referencia_atual += compra_produto.preco_unitario * compra_produto.quantidade
        gasto_referencia_passada = 0
        for compra in Compra.objects.filter(colaborador=colaborador, data__range=[get_referencia_passada(referencia_atual), referencia_atual]):
            for compra_produto in compra.compra_produtos.all():
                gasto_referencia_passada += compra_produto.preco_unitario * compra_produto.quantidade
        context = {
            'carrinho': request.session.get('carrinho', []),
            'gasto_mensal': gasto_referencia_atual,
            'gasto_referencia_passada': gasto_referencia_passada
        }
        return render(request, 'carrinho/carrinho.html', context)


def _get_colaborador_valido(request, login, senha):
    try:
        colaborador = Colaborador.objects.get(login=login)
    except Colaborador.DoesNotExist:
        messages.error(request, 'Colaborador não cadastrado.')
        return None
    if colaborador.situacao == 'inativo':
        messages.error(request, 'Colaborador inativo.')
        return None
    if not check_password(senha, colaborador.senha):
        messages.error(request, 'Senha incorreta.')
        return None
    return colaborador
