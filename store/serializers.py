from rest_framework import serializers
from  .models import *

# CategorySerializer
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["category_id", "category_title", "slug"]

# ProductSerializer
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = [ "product_id", "product_title", "slug", "category", "short_description", "description", "stock", "price", "old_price", "image",  "is_available", "top_deal", "flash_sales"]
    
    # category = CategorySerializer()

# VariationCategorySerializer
class VariationCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariationCategory
        fields = ['id', 'variation_category_title']


# ProductVaraiationSerializer
class ProductVaraiationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariation
        fields = ['variation_id', 'variation_value', 'variation_category', 'price', 'product', 'is_active']
    
    product = ProductSerializer()
