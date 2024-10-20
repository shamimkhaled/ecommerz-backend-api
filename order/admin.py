from django.contrib import admin
from .models import Shipping, Orders, OrderItem

# Register your models here.

class ShippingAdmin(admin.ModelAdmin):
    list_display = ('name', 'rate', 'estimated_delivery_days')
    list_display_links = ('name', 'rate')
    # readonly_fields = ('valid_from', 'valid_to', 'active' )
    # search_fields = ('cart__car_id', 'product__product_id')

    ordering = ('-name',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'user', 'cart', 'order_status', 'total_amount', 'grand_total', 'shipping_address', 'order_placed_at', 'updated_at')
    list_display_links = ('order_id', 'user')
    # readonly_fields = ('valid_from', 'valid_to', 'active' )
    # search_fields = ('cart__car_id', 'product__product_id')

    ordering = ('-order_placed_at',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'user', 'cart', 'order_status', 'total_amount', 'grand_total', 'shipping_address', 'order_placed_at', 'updated_at')
    list_display_links = ('order_id', 'user')
    # readonly_fields = ('valid_from', 'valid_to', 'active' )
    # search_fields = ('cart__car_id', 'product__product_id')

    ordering = ('-order_placed_at',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'product_variation', 'quantity', 'price', 'sub_total')
    list_display_links = ('order', 'product')
    # readonly_fields = ('valid_from', 'valid_to', 'active' )
    # search_fields = ('cart__car_id', 'product__product_id')

    # ordering = ('-order',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(Shipping, ShippingAdmin)
admin.site.register(Orders, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)