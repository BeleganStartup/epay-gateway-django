
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from chargily_epay_gateway_django.utils import get_api_key, get_secret_key
from chargily_epay_gateway.api import Invoice


class CSRFExemptInvoiceView(Invoice, View):
    API_KEY = get_api_key()

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(InvoiceView, self).dispatch(request, *args, **kwargs)


class InvoiceView(Invoice, View):
    API_KEY = get_api_key()


class WebhookView(View):
    SECRET_KEY = get_secret_key()

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(WebhookView, self).dispatch(request, *args, **kwargs)
