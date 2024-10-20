from dataclasses import field
from django.forms.models import ModelForm
from order.models import (
    Orders, 
    OrderItem, 
    Shipping,
   
)
from django import forms


class ShippingForm(ModelForm):
    class Meta:
        model = Shipping
        fields = ('__all__')

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'rate': forms.NumberInput(attrs={'class': 'form-control'}),
            'estimated_delivery_days': forms.TextInput(attrs={'class': 'form-control'}),
    

        }

class OrderForm(ModelForm):
    class Meta:
        model = Orders
        fields = ('__all__')

        widgets = {
            'shipping_address': forms.TextInput(attrs={'class': 'form-control'}),
            'user': forms.Select(attrs={'class': 'form-control'}),
            'cart': forms.Select(attrs={'class': 'form-control'}),
            'shipping_cost': forms.Select(attrs={'class': 'form-control'}),
            'order_status': forms.Select(attrs={'class': 'form-control'}),

            'total_amount': forms.NumberInput(attrs={'class': 'form-control'}),

            'grand_total': forms.NumberInput(attrs={'class': 'form-control'}),

         }
        


class OrderItemForm(ModelForm):
    class Meta:
        model = OrderItem
        fields = ('__all__')

        widgets = {
            'order': forms.Select(attrs={'class': 'form-control'}),
            'product': forms.Select(attrs={'class': 'form-control'}),
            'product_variation': forms.Select(attrs={'class': 'form-control'}),

            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),

            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'sub_total': forms.NumberInput(attrs={'class': 'form-control'}),

         }        