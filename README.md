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
4. Our package ![chargily-epay-gateway](https://pypi.org/project/chargily-epay-gateway/ "Chargily ePay Gateway package") for python.

# Installation
Using pip
```bash
pip install chargily-epay-gateway-django
```

or pipenv
```bash
pipenv install chargily-epay-gateway-django
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
from chargily_epay_gateway_django.forms import InvoiceForm

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

2- Validate Chargily Signature:

```python
from chargily_epay_gateway.api import webhook_is_valid

# Return True if signature is valid, otherwise False
valid_signature = webhook_is_valid(request)
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


# TODO

1- Create Invoice Model
2- Create Webhook view
3- Website urls settings (Try to retreive dynamically)
4- Complete Webhook documentation
