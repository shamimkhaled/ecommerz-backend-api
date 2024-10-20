from dataclasses import field
from django.forms.models import ModelForm
from cart.models import (
    Carts, 
    CartItem, 
    
   
)
from django import forms



class CartForm(ModelForm):
    class Meta:
        model = Carts
        fields = ('__all__')

        widgets = {
            
            'user': forms.Select(attrs={'class': 'form-control'}),
            'coupon': forms.Select(attrs={'class': 'form-control'}),

         }
        

class CartItemForm(ModelForm):
    class Meta:
        model = CartItem
        fields = ('__all__')
        # exclude = ['slug']

        widgets = {
            
            'cart': forms.Select(attrs={'class': 'form-control'}),
            'product': forms.Select(attrs={'class': 'form-control'}),
            'product_variation': forms.Select(attrs={'class': 'form-control'}),
            
        }
