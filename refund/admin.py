from django.contrib import admin
from .models import Refunds, RefundItems


# Register your models here.
class RefundsAdmin(admin.ModelAdmin):
    list_display = ('order', 'transaction_id', 'reason', 'amount', 'status', 'requested_by', 'requested_at', 'processed_by', 'processed_at')
    list_display_links = ('order', 'transaction_id')
    readonly_fields = ('reason', 'amount', 'status', 'requested_by', 'requested_at', 'processed_by', 'processed_at')
    search_fields = ('order__order_id', 'transaction__transaction_id')

    ordering = ('-requested_at',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(Refunds, RefundsAdmin)
admin.site.register(RefundItems)

