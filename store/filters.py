from django_filters.rest_framework import FilterSet
from .models import Products
import django_filters



class ProductFilters(FilterSet):
    product_title = django_filters.CharFilter(field_name='product_title', lookup_expr='icontains')
    category_id = django_filters.UUIDFilter(field_name='category_id')
    price_min = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    price_max = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    ordering = django_filters.OrderingFilter(
        fields=(
            ('price', 'price'),
            ('created_at', 'created_at'),
        ),
    )

    class Meta:
        model = Products
        fields = ['product_title', 'category_id', 'price_min', 'price_max', 'ordering']

    # class Meta:
    #     model = Products
    #     fields = {
    #         'category_id': ['exact'],
    #         'price': ['gt', 'lt']
    #     }






        #   ======APIVIEW====

        # filterset = ProductFilters(request.GET, queryset=product)
        # if filterset.is_valid():
        #     product = filterset.qs
        
        # #  search
        # search = request.GET.get('search', '')
        # if search:
        #     product = product.filter(title__icontains=search) | product.filter(short_description__icontains=search) | product.filter(description__icontains=search)
        
        # #  ordering/sorting
        # ordering = request.GET.get('ordering', '')
        # if ordering:
        #     product = product.order_by(ordering)