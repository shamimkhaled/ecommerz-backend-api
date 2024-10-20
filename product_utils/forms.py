from dataclasses import field
from django.forms.models import ModelForm
from .models import (
    Wishlist, 
    Compare, 
    Review,
   
)
from store.models import Products
from django import forms


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ('__all__')

        widgets = {
            'user': forms.Select(attrs={'class': 'form-control'}),
            'product': forms.Select(attrs={'class': 'form-control'}),
            'rating': forms.Select(attrs={'class': 'form-control'}),
            'payment_status': forms.Select(attrs={'class': 'form-control'}),
            'comment': forms.TextInput(attrs={'class': 'form-control'}),
            

        }

class WishlistForm(ModelForm):
   
    class Meta:
        model = Wishlist
        fields = ('__all__')

        widgets = {
            # 'products': forms.TextInput(attrs={'class': 'form-control'}),
            'user': forms.Select(attrs={'class': 'form-control'}),
          
         }
        

class CompareForm(ModelForm):

    
    class Meta:
        model = Compare
        fields = ('__all__')

        widgets = {
            # 'products': forms.TextInput(attrs={'class': 'form-control'}),
            'user': forms.Select(attrs={'class': 'form-control'}),
          
         }
