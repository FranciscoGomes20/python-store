import stripe
from django.conf import settings  # alterar settings quando for upar no heroku
from django.http import JsonResponse
from django.views import View
from django.views.generic import TemplateView
from .models import Produto
from django.shortcuts import render


stripe.api_key = settings.STRIPE_SECRET_KEY


class SucessoView(TemplateView):
    template_name = 'sucesso.html'


class CanceladoView(TemplateView):
    template_name = 'cancelado.html'


class index(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        produto = Produto.objects.get(nome="Teste")
        context = super(index, self).get_context_data(**kwargs)
        context.update({
            "produto": produto,
            "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY
        })
        return context


class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        produto_id = self.kwargs["pk"]
        produto = Produto.objects.get(id=produto_id)
        print(produto)
        YOUR_DOMAIN = "http://127.0.0.1:8000"
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'brl',
                        'unit_amount': produto.preco,
                        'product_data': {
                            'name': produto.nome,
                            # 'images': ['https://i.imgur.com/EHyR2nP.png'], descomentar caso queria adicionar imagem do produto no checkout
                        },
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=YOUR_DOMAIN + '/sucesso/',
            cancel_url=YOUR_DOMAIN + '/cancelado/',
        )
        return JsonResponse({
            'id': checkout_session.id
        })

def base(request):
    return render(request, 'base.html')