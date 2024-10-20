from dataclasses import field
from django.forms.models import ModelForm
from payment.models import (
    Payment, 
    BillingAddress, 
   
)
from django import forms


class PaymentForm(ModelForm):
    class Meta:
        model = Payment
        fields = ('__all__')

        widgets = {
            'user': forms.Select(attrs={'class': 'form-control'}),
            'order': forms.Select(attrs={'class': 'form-control'}),
            'payment_method': forms.Select(attrs={'class': 'form-control'}),
            'payment_status': forms.Select(attrs={'class': 'form-control'}),
            'transaction_id': forms.TextInput(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'estimated_delivery_days': forms.TextInput(attrs={'class': 'form-control'}),
    

        }

class BillingAddressForm(ModelForm):
    class Meta:
        model = BillingAddress
        fields = ('__all__')

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'address1': forms.TextInput(attrs={'class': 'form-control'}),
            'address2': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'zipcode': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'user': forms.Select(attrs={'class': 'form-control'}),
          
         }
        

