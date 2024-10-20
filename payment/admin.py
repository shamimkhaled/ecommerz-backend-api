from django.contrib import admin
from .models import Payment, BillingAddress

# Register your models here.

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user','order', 'transaction_id', 'payment_status', 'amount', 'created_at')
    list_display_links = ('user', 'order', 'transaction_id')
    # readonly_fields = ('valid_from', 'valid_to', 'active' )
    # search_fields = ('order__order_id')

    ordering = ('-created_at',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


# class BillingAddressAdmin(admin.ModelAdmin):
#     list_display = ('user','order', 'transaction_id', 'payment_status', 'amount', 'created_at')
#     list_display_links = ('user', 'order', 'transaction_id')
#     # readonly_fields = ('valid_from', 'valid_to', 'active' )
#     # search_fields = ('order__order_id')

#     ordering = ('-created_at',)

#     filter_horizontal = ()
#     list_filter = ()
#     fieldsets = ()

admin.site.register(Payment, PaymentAdmin)
admin.site.register(BillingAddress)