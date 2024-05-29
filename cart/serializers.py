from rest_framework import serializers
from store.models import Products, ProductVariation
from store.serializers import ProductSerializer, ProductVaraiationSerializer
from .models import Carts, CartItem
from couponcode.models import Coupon
from django.utils import timezone




class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_variation = ProductVaraiationSerializer(read_only=True)
    sub_total = serializers.SerializerMethodField()


    class Meta:
        model = CartItem
        fields = ['id', 'cart', 'product', 'product_variation', 'quantity', 'sub_total']

    def get_sub_total(self, obj):
        return obj.sub_total()
    








class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(source='cartitems', many=True)
    total_price = serializers.SerializerMethodField()
    total_cartitems = serializers.SerializerMethodField()
    coupon = serializers.CharField(write_only=True, required=False)


    class Meta:
        model = Carts
        fields = ['cart_id', 'total_cartitems', 'user', 'items', 'total_price', 'coupon', 'created_at', 'updated_at']

    

    def get_total_price(self, cart):
        total = sum(item.sub_total() for item in cart.cartitems.all())
        if cart.coupon:
            discount = (total * cart.coupon.discount) / 100
            total -= discount
        return total

    
    def get_total_cartitems(self, cart):
        return sum(item.quantity for item in cart.cartitems.all())
    
    def get_coupon_code(self, cart):
        return cart.coupon.code if cart.coupon else None
    
  


# class AddCartItemSerializer(serializers.ModelSerializer):
#         product_id = serializers.UUIDField()
#         variation_id = serializers.UUIDField(required=False)


#         def validate_product_id(self, value):
#             if not Products.objects.filter(pk=value).exists():
#                 raise serializers.ValidationError("There is no product associated with the given ID")
#             return value
        
#         def validate(self, attrs):
#             product_id = attrs['product_id']
#             variation_id = attrs.get('variation_id')

#             # Check if product has variations
#             product = Products.objects.get(pk=product_id)

#             if product.has_variations:
#                 # Validate variation_id if provided
#                 if variation_id:
#                     if not ProductVariation.objects.filter(pk=variation_id, product=product).exists():
#                         raise serializers.ValidationError("Invalid variation ID for the chosen product")
#                 else:
#                     raise serializers.ValidationError("A variation ID is required for products with variations")

#             return attrs


#         def save(self, **kwargs):
#             cart_id = self.context["cart_id"]
#             product_id = self.validated_data["product_id"]
#             variation_id = self.validated_data.get("variation_id")
#             quantity = self.validated_data["quantity"]

#             try:
#                 # Try to get the existing cart item
#                 if variation_id:
#                     # Use variation_id for lookup if provided
#                     cart_item = CartItem.objects.get(product_id=product_id, variation_id=variation_id, cart_id=cart_id)
#                 else:
#                     # Use product_id for lookup if no variation selected
#                     cart_item = CartItem.objects.get(product_id=product_id, cart_id=cart_id)
#                 cart_item.quantity += quantity
#                 cart_item.save()
#                 self.instance = cart_item
#             except CartItem.DoesNotExist:
#                 # If cart item doesn't exist, create a new one
#                 if variation_id:
#                     self.instance = CartItem.objects.create(cart_id=cart_id, product_id=product_id, variation_id=variation_id, **self.validated_data)
#                 else:
#                     self.instance = CartItem.objects.create(cart_id=cart_id, product_id=product_id, **self.validated_data)

#             return self.instance
#         class Meta:
#             model = CartItem
#             fields = ["id", "product_id", "variation_id", "quantity"]



class AddCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.UUIDField()
    product_variation_id = serializers.UUIDField(required=False)

    def validate_product_id(self, value):
        if not Products.objects.filter(pk=value).exists():
            raise serializers.ValidationError("There is no product associated with the given ID")
        return value
    
    def validate_product_variation_id(self, value):
        if not ProductVariation.objects.filter(pk=value).exists():
            raise serializers.ValidationError("There is no product variation id associated with the given ID")
        
        return value



    def save(self, **kwargs):
        cart_id = self.context["cart_id"]
        product_id = self.validated_data["product_id"]
        product_variation_id = self.validated_data.get('product_variation_id')

        quantity = self.validated_data["quantity"]
        print(product_variation_id)

        if not product_variation_id:
            try:
                # Try to get the existing cart item
                cart_item = CartItem.objects.get( product_id=product_id, cart_id=cart_id)
                cart_item.quantity += quantity
                cart_item.save()
                self.instance = cart_item
            except CartItem.DoesNotExist:
                # If cart item doesn't exist, create a new one
                self.instance = CartItem.objects.create(cart_id=cart_id, **self.validated_data)
            return self.instance
        
        else:
            try:
                # Try to get the existing cart item
                cart_item = CartItem.objects.get(product_variation_id=product_variation_id, product_id=product_id, cart_id=cart_id)
                cart_item.quantity += quantity
                cart_item.save()
                self.instance = cart_item
            except CartItem.DoesNotExist:
                # If cart item doesn't exist, create a new one
                self.instance = CartItem.objects.create(cart_id=cart_id, **self.validated_data)
                
                return self.instance


    class Meta:
        model = CartItem
        fields = ["id", "product_id", "product_variation_id", "quantity"]

