from django.contrib import admin
from .models import Coupon

# Register your models here.
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount', 'valid_from', 'valid_to', 'active')
    list_display_links = ('code', 'discount')
    readonly_fields = ('valid_from', 'valid_to', 'active' )
    # search_fields = ('cart__car_id', 'product__product_id')

    ordering = ('-valid_from',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(Coupon, CouponAdmin)