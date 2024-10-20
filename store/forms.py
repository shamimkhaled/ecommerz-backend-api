from dataclasses import field
from django.forms.models import ModelForm
from store.models import (
    Category, 
    Products, 
    ProductVariation,
    ProductVariationCategory,
   
)
from django import forms



class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ('__all__')

        widgets = {
            'category_title': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'category_desc': forms.Textarea(attrs={'class': 'form-control'}),
            'parent': forms.Select(attrs={'class': 'form-control'}),
            'category_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),

         }
        

class ProductsForm(ModelForm):
    class Meta:
        model = Products
        fields = ('__all__')
        exclude = ['slug']

        widgets = {
            'product_title': forms.TextInput(attrs={'class': 'form-control'}),
            'short_description': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'old_price': forms.NumberInput(attrs={'class': 'form-control'}),
            # 'is_available': forms.CheckboxInput(attrs={'class': 'form-control'}),
            # 'top_deal': forms.CheckboxInput(attrs={'class': 'form-control'}),
            # 'flash_sales': forms.CheckboxInput(attrs={'class': 'form-control'}),
            # 'is_out_of_stock': forms.CheckboxInput(attrs={'class': 'form-control'}),
        }


class ProductVariationForm(ModelForm):
    class Meta:
        model = ProductVariation
        fields = ('__all__')

        widgets = {
            'variation_value': forms.TextInput(attrs={'class': 'form-control'}),
            'variation_category': forms.Select(attrs={'class': 'form-control'}),
            'product': forms.Select(attrs={'class': 'form-control'}),


            'price': forms.NumberInput(attrs={'class': 'form-control'}),

        }
        

class VariationCategoryForm(ModelForm):
    class Meta:
        model = ProductVariationCategory
        fields = ('__all__')
        
        widgets = {
            'variation_category_title': forms.TextInput(attrs={'class': 'form-control'}),
        }
