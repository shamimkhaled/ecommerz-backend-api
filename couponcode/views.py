from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Coupon
from .serializers import CouponSerializer
from django.utils import timezone
from cart.models import Carts, CartItem
from cart.serializers import CartSerializer, CartItemSerializer
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth import get_user_model
from django.conf import settings
import jwt


class CouponListCreateAPIView(APIView):

    def get(self, request):
        coupons = Coupon.objects.all()
        serializer = CouponSerializer(coupons, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CouponSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CouponDetailAPIView(APIView):
    def get(self, request, coupon_id):
        coupon = get_object_or_404(Coupon, id=coupon_id)
        serializer = CouponSerializer(coupon)
        return Response(serializer.data)

    def put(self, request, coupon_id):
        coupon = get_object_or_404(Coupon, id=coupon_id)
        serializer = CouponSerializer(coupon, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, coupon_id):
        coupon = get_object_or_404(Coupon, id=coupon_id)
        coupon.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)





# class ApplyCouponCodeView(APIView):

#     def post(self, request, cart_id):
#         cart = get_object_or_404(Carts, pk=cart_id)
#         coupon_code = request.data.get('coupon_code', '')

#         if not coupon_code:
#             return Response({"error": "Coupon code is required"}, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             coupon = Coupon.objects.get(code=coupon_code, active=True)
#             if not (coupon.valid_from <= timezone.now() <= coupon.valid_to):
#                 return Response({"error": "Coupon is not valid at this time"}, status=status.HTTP_400_BAD_REQUEST)
#         except Coupon.DoesNotExist:
#             return Response({"error": "Invalid coupon code"}, status=status.HTTP_400_BAD_REQUEST)

#         # Calculate the new total price with the coupon applied
#         total_price = sum(item.sub_total() for item in cart.cartitems.all())
#         discount = (total_price * coupon.discount) / 100
#         total_price -= discount

#         # Update the cart serializer with the new total price
#         serializer = CartSerializer(cart, context={'request': request})
#         cart_data = serializer.data
#         cart_data['total_price'] = total_price  # Overwrite the total price with the discounted price

#         return Response(cart_data, status=status.HTTP_200_OK)
