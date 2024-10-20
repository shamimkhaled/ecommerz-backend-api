from dataclasses import field
from django.forms.models import ModelForm
from accounts.models import (
    UserAccount, UserProfile,
   
)
from django import forms


class UserForm(ModelForm):
    class Meta:
        model = UserAccount
        fields = ('__all__')

        # widgets = {
        #     'user': forms.Select(attrs={'class': 'form-control'}),
        #     'order': forms.Select(attrs={'class': 'form-control'}),
        #     'payment_method': forms.Select(attrs={'class': 'form-control'}),
        #     'payment_status': forms.Select(attrs={'class': 'form-control'}),
        #     'transaction_id': forms.TextInput(attrs={'class': 'form-control'}),
        #     'amount': forms.NumberInput(attrs={'class': 'form-control'}),
        #     'estimated_delivery_days': forms.TextInput(attrs={'class': 'form-control'}),
    

        # }

