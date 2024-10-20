from rest_framework import serializers
from .models import Review, Wishlist, Compare
from store.models import Products
from store.serializers import ProductSerializer
from accounts.models import UserAccount


# ===============================ReviewSerializer==================================
class ReviewSerializer(serializers.ModelSerializer):
    # product = ProductSerializer(read_only=True)
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'product', 'user', 'rating', 'comment', 'created_at', 'updated_at']


# ===============================WishlistSerializer==================================

class WishlistSerializer(serializers.ModelSerializer):
    products = serializers.PrimaryKeyRelatedField(queryset=Products.objects.all(), many=True)
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Wishlist
        fields = ['id', 'user', 'products']



# ===================================CompareSerializer=================================
class CompareSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    products = ProductSerializer(many=True)

    class Meta:
        model = Compare
        fields = ['id', 'user', 'products']
