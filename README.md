# epay-gateway-django
Chargily ePay Gateway (Django Package)

![Chargily ePay Gateway](https://raw.githubusercontent.com/Chargily/epay-gateway-php/main/assets/banner-1544x500.png "Chargily ePay Gateway")

This Plugin is to integrate ePayment gateway with Chargily easily.
- Currently support payment by **CIB / EDAHABIA** cards and soon by **Visa / Mastercard** 
- This repo is recently created for **Django plugin**, If you are a developer and want to collaborate to the development of this plugin, you are welcomed!

# Requirements
1. Python 2.7 or higher.
2. Django 1.11 or higher.
3. API Key/Secret from [ePay by Chargily](https://epay.chargily.com.dz) dashboard for free.
4. Our package [chargily-epay-gateway](https://pypi.org/project/chargily-epay-gateway/) for python.

# Installation
Using pip
```bash
pip install chargily-epay-gateway-django-plugin
```

or pipenv
```bash
pipenv install chargily-epay-gateway-django-plugin
```

# Quick start
1- Make sure to secure your credentials by setting up the Environment Variables or using `.env` file.

2- Load `CHARGILY_APP_KEY` and `CHARGILY_APP_SECRET` environment variables in settings.py file.


# Usage
1- Make Payment:

- You can use class or function based view to make a payment
- If you are using `POST` method, make sure to *disable Django's CSRF validation*.

* Class based View Example

- In `views.py` :
```python
from django.shortcuts import render

from chargily_epay_gateway_django.views import InvoiceView
from chargily_epay_gateway_django.forms import InvoiceForm  # You can customize this form if you like

class MakePayment(InvoiceView):

    def get(self, request):
        form = InvoiceForm()
        context = {
            'form': form,
        }
        return render(request, 'payment.html', context)

    def post(self, request):
        form = InvoiceForm(data=request.POST) 
        context = {
            'form': form,
            'data': None,
            'errors': None,
        }
        if form.is_valid():
            invoice = self.make_payment(**form.data)
            response = self.load_invoice(invoice.content)
            if invoice.status_code == 201:
                context['data'] = response['checkout_url']
            else:
                context['errors'] = [value for value in response['errors'].items()]
        return render(request, 'payment.html', context)
```

Output example:

* Wrong inputs
![Wrong inputs](https://scontent.fist4-1.fna.fbcdn.net/v/t1.15752-9/279546536_515119966919096_4807134273052621412_n.png?_nc_cat=105&ccb=1-5&_nc_sid=ae9488&_nc_ohc=liw7awHFEYQAX-2qawy&_nc_ht=scontent.fist4-1.fna&oh=03_AVJIc7iZ4U5-QziGdKiYJhWi0Sz93TfSb1bHgYvOwZ-P4Q&oe=6296BE5C "Wrong inputs")

* Correct inputs
![Correct inputs](https://scontent.fist4-1.fna.fbcdn.net/v/t1.15752-9/278810906_1152322268902183_4302638377087918631_n.png?_nc_cat=101&ccb=1-5&_nc_sid=ae9488&_nc_ohc=pr6kUJl0AHEAX_S6Ruj&_nc_ht=scontent.fist4-1.fna&oh=03_AVKEw5KRilzBeuIE-Ei37tLwuWaq-z1_CT-Jn8WTeZ_z0A&oe=629821F9 "Correct inputs")

> You can use `CSRFExemptInvoiceView` instead of `InvoiceView` if you want to ignore csrf validation.

- in `payment.html`:
```html
<form method="POST" >

    {% csrf_token %}
    {{form.as_p}}
    <input type="submit" value="MAKE PAYMENT">

    <!-- Handle Data -->
    {% if data %}
        <p><a target='__blank' href='{{data}}'>{{data}}</a></p>
    {% endif %}

    <!-- Handle Errors -->
    {% if errors %}
    <ul>
        {% for error in errors %}
            <li>{{error}}</li>
        {% endfor %}
    </ul>
    {% endif %}

</form>
```


- If you want to return JSON instead, you can use it like this:
```Python
from django.http import JsonResponse

from chargily_epay_gateway_django.views import InvoiceView


class MakePayment(InvoiceView):

    def post(self, request):
        invoice = self.make_payment(  # You can use InvoiceForm
            client='Client Name',
            client_email='Client Email',
            invoice_number='Invoice ID',
            amount='Amount',
            discount='Discount',
            back_url='https://example.com/',
            webhook_url='https://example.com/webhook/',
            mode="CIB",
            comment='for integration test',
        )
        return JsonResponse(self.load_invoice(invoice.content))
```

* Function based view

```python
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from chargily_epay_gateway.api import make_payment

@csrf_exempt
def invoice(request):
    if request.method != 'POST':
        return JsonResponse({'message': 'Method {} not allowed'.format(request.method)}, status=403)
    response = make_payment(  # You can use InvoiceForm
        client='Client Name',
        client_email='Client Email',
        invoice_number='Invoice ID',
        amount='Amount',
        discount='Discount',
        back_url='https://example.com/',
        webhook_url='https://example.com/webhook/',
        mode="CIB",
        comment='for integration test',
    )
    return JsonResponse(response.json(), status=response.status_code)
```

2- Webhook Usage:

```python
from django.http import JsonResponse

from chargily_epay_gateway_django.views import WebhookView

from chargily_epay_gateway.utils import signature_is_valid


class ChargilyReceiver(WebhookView):

    def post(self, request):
        valid_signature = signature_is_valid(self.SECRET_KEY, request)
        if valid_signature:
            ...
            # Do whatever you want
        return JsonResponse({}, status=200)
```

3- Don't forget to register your views in urls.py
```python
from django.urls import path

from your_app.views import MakePayment, ChargilyReceiver


urlpatterns = [
    path('payment/', MakePayment.as_view(), name='payment'),
    path('webhook/', ChargilyReceiver.as_view(), name='webhook'),
]
```


# Configurations

- Available Configurations

| key                   |  description                                                                                          | redirect url |  process url |
|-----------------------|-------------------------------------------------------------------------------------------------------|--------------|--------------|
| CHARGILY_APP_KEY               | must be string given by organization                                                                  |   required   |   required   |
| CHARGILY_APP_SECRET            | must be string given by organization                                                                  |   required   |   required   |
| back_url        | must be string and valid url                                                                          |   required   | not required |
| webhook_url        | must be string and valid url                                                                          _|   required   | required |
| mode                  | must be in **CIB**,**EDAHABIA**                                                                       |   required   | not required |
| invoice_number       |  string or int                                                                                 |   required   | not required |
| client_name  | string                                                                                        |   required   | not required |
| clientEmail | must be valid email This is where client receive payment receipt after confirmation        |   required   | not required |
| amount      | must be numeric and greather or equal than  75                                                        |   required   | not required |
| discount    | must be numeric and between 0 and 99  (discount in %)                                     |   required   | not required |
| description  | must be string_                                                                                        |   required   | not required |


# Notice

- If you faced Issues [Click here to open one](https://github.com/Chargily/epay-gateway-django)
