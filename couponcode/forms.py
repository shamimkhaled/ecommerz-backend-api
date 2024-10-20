from dataclasses import field
from django.forms.models import ModelForm
from couponcode.models import (
    Coupon, 
    
    
   
)
from django import forms
from django.utils import timezone



class CouponCodeForm(ModelForm):
    class Meta:
        model = Coupon
        fields = ('__all__')

        widgets = {
            
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'discount': forms.NumberInput(attrs={'class': 'form-control'}),
            'valid_from': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'valid_to': forms.DateTimeInput(attrs={
                'class': 'form-control', 
                'type': 'datetime-local'
                # 'format': '%Y-%m-%dT%H:%M'
            }),
            'active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),

         }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.initial.get('valid_from'):
            self.initial['valid_from'] = timezone.now().strftime('%Y-%m-%dT%H:%M')
        if not self.initial.get('valid_to'):
            self.initial['valid_to'] = timezone.now().strftime('%Y-%m-%dT%H:%M')