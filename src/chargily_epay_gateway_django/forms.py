
from django import forms


class InvoiceForm(forms.Form):
    client=forms.CharField()
    client_email=forms.EmailField()
    invoice_number=forms.IntegerField()
    amount=forms.FloatField()
    discount=forms.FloatField()
    back_url=forms.CharField()
    webhook_url=forms.CharField()
    mode=forms.CharField()
    comment=forms.CharField()
