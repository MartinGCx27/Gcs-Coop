import pdb
import stripe
from django.conf import settings
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.views import View
from django.views.generic import TemplateView
from .models import Price, Product
# Validate contracts function
from dashboard.views import contracts_validation

# Inscripcion
from catalogues.models import EnrollmentCatalogue
# Mensualidad
from coop_info.models import CotImssRelation

stripe.api_key = settings.STRIPE_SECRET_KEY


class SuccessView(TemplateView):
    template_name = "runway/success.html"


class CancelView(TemplateView):
    template_name = "runway/cancel.html"


class HighwayView(TemplateView):
    template_name = "runway/highway.html"

    @method_decorator(login_required)
    @method_decorator(staff_member_required())
    def get(self, request, *args, **kwargs):
        # Obtenemos informacion User
        user = User.objects.get(id=request.user.id)

        return user
        # return render(request, "runway/highway.html")


class ProductLandingPageView(TemplateView):
    template_name = "runway/landing.html"

    def get_context_data(self, **kwargs):
        product = Product.objects.get(name="Test Product")
        prices = Price.objects.filter(product=product)
        context = super(ProductLandingPageView,
                        self).get_context_data(**kwargs)
        context.update({
            "product": product,
            "prices": prices
        })
        return context


class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        price = Price.objects.get(id=self.kwargs["pk"])
        YOUR_DOMAIN = "http://127.0.0.1:8000"  # change in production

        if self.kwargs["pk"] == '1':
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[
                    {
                        'price': price.stripe_price_id,
                        'quantity': 1,
                    },
                ],
                mode='payment',
                success_url=YOUR_DOMAIN + '/runway/success/',
                cancel_url=YOUR_DOMAIN + '/runway/cancel/',
            )
            return redirect(checkout_session.url)

        else:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[
                    {
                        'price': price.stripe_price_id,
                        'quantity': 1,
                    },
                ],
                mode='subscription',
                success_url=YOUR_DOMAIN + '/runway/success/',
                cancel_url=YOUR_DOMAIN + '/runway/cancel/',
            )

        return redirect(checkout_session.url)


class QueryContributionView(View):

    def get(self, request, *args, **kwargs):
        # Obtenemos informacion User
        user = User.objects.get(id=request.user.id)
        data_imss = CotImssRelation.objects.filter(user=user)
        # Validamos los contratos
        validate_contracts = contracts_validation(request.user.id)

        # Validamos si tiene datos requeridos para pagar
        dict_contribution = dict()

        if validate_contracts['contracts_val']:
            dict_contribution['validate'] = True
            dict_contribution['cotization'] = data_imss[0].cotizacion_imss.salario_cot.veces
            dict_contribution['amount'] = data_imss[0].cotizacion_imss.salario_cot.aport_coop

            # Asignamos cada enlace
            if dict_contribution['cotization'] == 0.0:
                dict_contribution['link'] = "https://buy.stripe.com/8wMg1Eb1ja8H2Iw00c"
                dict_contribution['recurrent_link'] = "https://buy.stripe.com/14kbLo9Xfa8HerefZu"
            elif dict_contribution['cotization'] == 1.0:
                dict_contribution['link'] = "https://buy.stripe.com/bIY4iW0mFcgPere6oz"
                dict_contribution['recurrent_link'] = "https://buy.stripe.com/28o16KfhzbcL3MAbJf"
            elif dict_contribution['cotization'] == 1.5:
                dict_contribution['link'] = "https://buy.stripe.com/00geXAedv0y73MA6oB"
                dict_contribution['recurrent_link'] = "https://buy.stripe.com/cN2eXA0mF6Wv5UI6oW"
            elif dict_contribution['cotization'] == 2.0:
                dict_contribution['link'] = "https://buy.stripe.com/28o2aO3yRcgP2IwaES"
                dict_contribution['recurrent_link'] = "https://buy.stripe.com/4gweXA0mF94Dgzm8x5"
            elif dict_contribution['cotization'] == 2.5:
                dict_contribution['link'] = "https://buy.stripe.com/eVa2aO9Xf94D0AoaEU"
                dict_contribution['recurrent_link'] = "https://buy.stripe.com/7sI02G9Xfa8HdnabJi"
            elif dict_contribution['cotization'] == 3.0:
                dict_contribution['link'] = "https://buy.stripe.com/4gw8zc3yR6Wv1EscN7"
                dict_contribution['recurrent_link'] = "https://buy.stripe.com/5kA02G3yR3Kj96UaET"
            elif dict_contribution['cotization'] == 3.5:
                dict_contribution['link'] = "https://buy.stripe.com/00g9DgfhzdkT6YM4gx"
                dict_contribution['recurrent_link'] = "https://buy.stripe.com/5kA16KedvdkT82QeVv"
            elif dict_contribution['cotization'] == 4.0:
                dict_contribution['link'] = "https://buy.stripe.com/8wM7v87P72Gfcj63cu"
                dict_contribution['recurrent_link'] = "https://buy.stripe.com/9AQ3eSd9rft196U3cO"
            elif dict_contribution['cotization'] == 4.5:
                dict_contribution['link'] = "https://buy.stripe.com/dR6g1E6L36Wv82Q5kD"
                dict_contribution['recurrent_link'] = "https://buy.stripe.com/3cs16K6L35Sr4QEfZB"
            elif dict_contribution['cotization'] == 5.0:
                dict_contribution['link'] = "https://buy.stripe.com/6oEcPsedvcgPdnaaEY"
                dict_contribution['recurrent_link'] = "https://buy.stripe.com/9AQ8zcedv94DaaY5kY"
            elif dict_contribution['cotization'] == 5.5:
                dict_contribution['link'] = "https://buy.stripe.com/5kA6r43yR3Kjgzm8wx"
                dict_contribution['recurrent_link'] = "https://buy.stripe.com/8wM16K3yR1Cb96UaF0"
            elif dict_contribution['cotization'] == 6.0:
                dict_contribution['link'] = "https://buy.stripe.com/3csg1EglD80zere5km"
                dict_contribution['recurrent_link'] = "https://buy.stripe.com/fZe2aOglD6Wv3MA7sP"
            elif dict_contribution['cotization'] == 6.5:
                dict_contribution['link'] = "https://buy.stripe.com/dR6cPs0mFgx5fvi9AD"
                dict_contribution['recurrent_link'] = "https://buy.stripe.com/bIYdTw9Xf2GfaaY00o"
            elif dict_contribution['cotization'] == 7.0:
                dict_contribution['link'] = "https://buy.stripe.com/14kcPs8Tb2Gf6YM28c"
                dict_contribution['recurrent_link'] = "https://buy.stripe.com/00gaHk0mFgx5aaY6oN"
            elif dict_contribution['cotization'] == 7.5:
                dict_contribution['link'] = "https://buy.stripe.com/6oEg1E2uN3Kjgzm149"
                dict_contribution['recurrent_link'] = "https://buy.stripe.com/aEU4iW9Xf3Kjcj67sS"
            elif dict_contribution['cotization'] == 8.0:
                dict_contribution['link'] = "https://buy.stripe.com/9AQ9Dgc5n5Srdna14a"
                dict_contribution['recurrent_link'] = "https://buy.stripe.com/14kcPsfhz0y7aaY5kL"
            elif dict_contribution['cotization'] == 8.5:
                dict_contribution['link'] = "https://buy.stripe.com/3cs4iW3yR1Cb96UbIP"
                dict_contribution['recurrent_link'] = "https://buy.stripe.com/eVa16K6L32Gfcj6aF6"
            elif dict_contribution['cotization'] == 9.0:
                dict_contribution['link'] = "https://buy.stripe.com/7sIbLo6L36Wv3MAfZ6"
                dict_contribution['recurrent_link'] = "https://buy.stripe.com/eVa9Dgc5n4Oncj65kN"
            elif dict_contribution['cotization'] == 9.5:
                dict_contribution['link'] = "https://buy.stripe.com/3cs2aOfhzcgP4QE28h"
                dict_contribution['recurrent_link'] = "https://buy.stripe.com/5kA2aO2uN2Gf4QEaF8"
            elif dict_contribution['cotization'] == 10.0:
                dict_contribution['link'] = "https://buy.stripe.com/00geXA4CV0y76YM4gq"
                dict_contribution['recurrent_link'] = "https://buy.stripe.com/dR6g1E5GZ1Cbbf2aF9"

        else:
            dict_contribution['validate'] = False

            if not validate_contracts['val_contract_coop']:
                dict_contribution['msg_contract_coop'] = validate_contracts['msg_contract_coop']
            else:
                dict_contribution['msg_contract_coop'] = ''

            if not validate_contracts['val_contract_user']:
                dict_contribution['msg_contract_user'] = validate_contracts['msg_contract_user']
            else:
                dict_contribution['msg_contract_user'] = ''

        # pdb.set_trace()

        return JsonResponse(dict_contribution)
