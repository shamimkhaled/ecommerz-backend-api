from django.contrib import admin
from .models import Carts, CartItem

# Register your models here.

class CartsAdmin(admin.ModelAdmin):
    list_display = ('cart_id', 'user', 'created_at', 'updated_at')
    list_display_links = ('cart_id', 'user')
    readonly_fields = ('created_at', 'updated_at', 'coupon' )
    # search_fields = ('order__order_id', 'transaction__transaction_id')

    ordering = ('-created_at',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()



class CartItemsAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'product_variation', 'quantity', 'sub_total', 'created_at', 'updated_at')
    list_display_links = ('cart', 'product')
    readonly_fields = ('created_at', 'updated_at', 'sub_total', 'quantity' )
    search_fields = ('cart__car_id', 'product__product_id')

    ordering = ('-created_at',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(Carts, CartsAdmin)
admin.site.register(CartItem, CartItemsAdmin)