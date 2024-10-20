from django.contrib import admin

from .models import (Category, Products, ProductVariationCategory, ProductVariation, ProductImages)
# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_title', 'slug', 'updated_at')
    list_display_links = ('category_title',)
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


class ProductImagesAdmin(admin.StackedInline):
    model = ProductImages
    extra = 1




class ProductsAdmin(admin.ModelAdmin):
    inlines = [ProductImagesAdmin]
    list_display = ('product_title', 'slug', 'category', 'stock', 'price',  'is_available', 'top_deal', 'flash_sales', 'updated_at')
    list_display_links = ('product_title',)
    readonly_fields = ('created_at', 'updated_at')
    prepopulated_fields = {'slug': ('product_title',)}

    ordering = ('-created_at',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()






class ProductVariationCategoryAdmin(admin.ModelAdmin):
    list_display = ('variation_category_title', 'updated_at')
    list_display_links = ('variation_category_title',)
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()  

class ProductVariationAdmin(admin.ModelAdmin):
    list_display = ('variation_value', 'variation_category', 'is_active', 'updated_at')
    list_display_links = ('variation_value',)
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()    

admin.site.register(Category, CategoryAdmin)
admin.site.register(Products, ProductsAdmin)
admin.site.register(ProductVariationCategory, ProductVariationCategoryAdmin)
admin.site.register(ProductVariation, ProductVariationAdmin)
admin.site.register(ProductImages)

