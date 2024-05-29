from rest_framework import serializers
from .models import Review, Wishlist
from store.models import Products
from store.serializers import ProductSerializer
from accounts.models import UserAccount



class ReviewSerializer(serializers.ModelSerializer):
    # product = ProductSerializer(read_only=True)
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'product', 'user', 'rating', 'comment', 'created_at', 'updated_at']

class WishlistSerializer(serializers.ModelSerializer):
    products = serializers.PrimaryKeyRelatedField(queryset=Products.objects.all(), many=True)
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Wishlist
        fields = ['id', 'user', 'products']
