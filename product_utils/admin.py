from django.contrib import admin
from .models import Review, Wishlist, Compare
# Register your models here.

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product','user', 'rating', 'comment', 'created_at', 'updated_at')
    list_display_links = ('product', 'user')
    # readonly_fields = ('valid_from', 'valid_to', 'active' )
    # search_fields = ('order__order_id')

    ordering = ('-created_at',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


class CompareAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'get_products')
    list_display_links = ('user',)
    # readonly_fields = ('valid_from', 'valid_to', 'active' )
    search_fields = ('products__product_id',)

    # ordering = ('-created_at',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

    def get_products(self, obj):
        return ", ".join([str(product) for product in obj.products.all()])
    get_products.short_description = 'Products'



class WishlistAdmin(admin.ModelAdmin):
    list_display = ('id','user', 'get_products')
    list_display_links = ( 'user',)
    # readonly_fields = ('valid_from', 'valid_to', 'active' )
    # search_fields = ('products__product_id',)

    # ordering = ('-created_at',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

    def get_products(self, obj):
        return ", ".join([str(product) for product in obj.products.all()])
    get_products.short_description = 'Products'

admin.site.register(Review, ReviewAdmin)
admin.site.register(Wishlist, WishlistAdmin)

admin.site.register(Compare, CompareAdmin)



