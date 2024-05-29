# # from django.shortcuts import render
# # from rest_framework import viewsets
# # from .models import Order, OrderItems, Shipping
# # from .serializers import OrderSerializer, OrderItemSerializer, ShippingSerializer, CreateOrderSerializer, UpdateOrderSerializer
# # from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
# # from rest_framework.response import Response
# # from rest_framework.viewsets import ModelViewSet, GenericViewSet
# # import jwt
# # from rest_framework.response import Response
# # from rest_framework.exceptions import AuthenticationFailed
# # import logging
# # from django.conf import settings
# # from django.contrib.auth import get_user_model

# # # Create your views here.
# # class ShippingViewSet(viewsets.ModelViewSet):
# #     queryset = Shipping.objects.all()
# #     serializer_class = ShippingSerializer


    

# # class OrderItemsViewSet(viewsets.ModelViewSet):
# #     queryset = OrderItems.objects.all()
# #     serializer_class = OrderItemSerializer





# # class OrderViewSet(viewsets.ModelViewSet):
# #     permission_classes = [AllowAny]
# #     http_method_names = ["get", "patch", "post", "delete", "options", "head"]

# #     def get_user_from_token(self, request):
# #         user_token = request.COOKIES.get('access_token')
# #         if not user_token:
# #             raise AuthenticationFailed('Unauthenticated user.')

# #         try:
# #             payload = jwt.decode(user_token, settings.SECRET_KEY, algorithms=['HS256'])
# #         except jwt.ExpiredSignatureError:
# #             raise AuthenticationFailed('Token has expired.')
# #         except jwt.InvalidTokenError:
# #             raise AuthenticationFailed('Invalid token.')

# #         model = get_user_model()
# #         user = model.objects.filter(user_id=payload['user_id']).first()

# #         if not user:
# #             raise AuthenticationFailed('User not found.')

# #         return user

# #     def get_permissions(self):
# #         if self.request.method in ["PATCH", "DELETE"]:
# #             return [IsAdminUser()]
# #         return super().get_permissions()

# #     def create(self, request, *args, **kwargs):
# #         user = self.get_user_from_token(request)
# #         serializer = CreateOrderSerializer(data=request.data, context={"user_id": user.user_id})
# #         serializer.is_valid(raise_exception=True)
# #         order = serializer.save()
# #         response_serializer = OrderSerializer(order)
# #         return Response(response_serializer.data)

# #     def get_serializer_class(self):
# #         if self.request.method == 'POST':
# #             return CreateOrderSerializer
# #         elif self.request.method == 'PATCH':
# #             return UpdateOrderSerializer
# #         return OrderSerializer

# #     def get_queryset(self):
# #         user = self.get_user_from_token(self.request)
# #         if user.is_staff:
# #             return Order.objects.all()
# #         return Order.objects.filter(user=user)

# from rest_framework import serializers
# from rest_framework import generics, status
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated, AllowAny
# from rest_framework.authentication import TokenAuthentication
# from rest_framework.exceptions import AuthenticationFailed
# from .models import Order, OrderItems
# from .serializers import OrderSerializer
# from accounts.models import UserAccount
# from django.contrib.auth import get_user_model
# from django.conf import settings
# import jwt

# class OrderListCreateAPIView(generics.ListCreateAPIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [AllowAny]
#     serializer_class = OrderSerializer

#     def get_queryset(self):
#         return Order.objects.filter(user=self.request.user)

#     def perform_create(self, serializer):
#         user_token = self.request.COOKIES.get('access_token')
#         if not user_token:
#             raise AuthenticationFailed('Unauthenticated user.')

#         try:
#             payload = jwt.decode(user_token, settings.SECRET_KEY, algorithms=['HS256'])
#         except jwt.ExpiredSignatureError:
#             raise AuthenticationFailed('Token has expired.')
#         except jwt.InvalidTokenError:
#             raise AuthenticationFailed('Invalid token.')

#         model = get_user_model()
#         user = model.objects.filter(user_id=payload['user_id']).first()
#         if not user:
#             raise AuthenticationFailed('User not found.')

#         shipping_address = self.request.data.get('shipping_address')
#         order = Order.create_from_cart(user, shipping_address)
#         if order is None:
#             raise serializers.ValidationError("No active cart found for the user.")

#         serializer.instance = order

# class OrderDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]
#     queryset = Order.objects.all()
#     serializer_class = OrderSerializer

#     def get_object(self):
#         user_token = self.request.COOKIES.get('access_token')
#         if not user_token:
#             raise AuthenticationFailed('Unauthenticated user.')

#         try:
#             payload = jwt.decode(user_token, settings.SECRET_KEY, algorithms=['HS256'])
#         except jwt.ExpiredSignatureError:
#             raise AuthenticationFailed('Token has expired.')
#         except jwt.InvalidTokenError:
#             raise AuthenticationFailed('Invalid token.')

#         model = get_user_model()
#         user = model.objects.filter(user_id=payload['user_id']).first()
#         if not user:
#             raise AuthenticationFailed('User not found.')

#         obj = super().get_object()
#         if obj.user != user:
#             raise AuthenticationFailed('You do not have permission to access this order.')

#         return obj




from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings
import jwt
from django.db.models import Sum
from .models import Orders, OrderItem,  Shipping
from cart.models import Carts, CartItem
from cart.serializers import *
from .serializers import OrderSerializer, OrderItemSerializer
from django.contrib.auth import get_user_model
from rest_framework.authentication import TokenAuthentication
from .token_authentication import CustomTokenAuthentication




# =================================OrderViewSet=========================

class OrderViewSet(generics.CreateAPIView):
    serializer_class = OrderSerializer
    queryset = Orders.objects.all()
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]

   
    
    def get_object(self, pk, user):
        try:
            return Orders.objects.get(order_id=pk, user=user)
        except Orders.DoesNotExist:
            return None

    def perform_create(self, serializer):
        user = self.request.user

        # Authentication check moved before cart retrieval
        if not user:
            raise AuthenticationFailed('Unauthenticated user.')
        
        cart_id = self.request.data.get('cart')
    

        # Ensure the cart ID is provided
        if not cart_id:
            raise serializers.ValidationError('Cart ID is required.')

        # Check if the cart belongs to the user
        try:
            cart = Carts.objects.get(pk=cart_id, user=user)
        except Carts.DoesNotExist:
            raise serializers.ValidationError('Invalid cart ID.')
        
        if Orders.objects.filter(cart=cart).exists():
            raise serializers.ValidationError('This cart has already been used in an order.')
        
        shipping_cost_id = self.request.data.get('shipping_cost')
        shipping_cost = Shipping.objects.get(name=shipping_cost_id)


        # Calculate the total price with discount
        total_price = sum(item.sub_total() for item in cart.cartitems.all())
        if cart.coupon:
            discount = (total_price * cart.coupon.discount) / 100
            total_price -= discount

        if not total_price:
            raise serializers.ValidationError('Cart is empty. Add items to cart before placing an order.')

        # Calculate the grand total price with shipping cost
        grand_total = total_price + shipping_cost.rate



        order = serializer.save(user=user, total_amount=total_price, grand_total=grand_total, cart=cart, shipping_cost=shipping_cost)


        for cart_item in cart.cartitems.all():
            product = cart_item.product
            if product.stock < cart_item.quantity:
                raise serializers.ValidationError(f'Not enough stock for {product.product_title}. Available stock: {product.stock}')

            # Update the out of stock status if necessary
            product.stock -= cart_item.quantity
            product.check_stock()  
            product.save()


        for cart_item in cart.cartitems.all():
            order_item_data = {
                'order': order.order_id,
                'product': cart_item.product.product_id,
                'product_variation': cart_item.product_variation,
                'quantity': cart_item.quantity,
                'price': cart_item.sub_total()
            }

            order_item_serializer = OrderItemSerializer(data=order_item_data)
            order_item_serializer.is_valid(raise_exception=True)
            order_item_serializer.save()

        # Clear cart items after successful order creation
        cart.cartitems.all().delete()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    
    def get_permissions(self):
        if self.request.method in ['PATCH', 'DELETE']:
            return [IsAdminUser()]
        return [IsAuthenticated()]
    

    


class OrderListViewSet(generics.ListAPIView):
    serializer_class = OrderSerializer
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get_user_from_token(self, request):
        user_token = request.COOKIES.get('access_token')
        if not user_token:
            raise AuthenticationFailed('Unauthenticated user.')

        try:
            payload = jwt.decode(user_token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token has expired.')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Invalid token.')

        model = get_user_model()
        user = model.objects.filter(user_id=payload['user_id']).first()

        if not user:
            raise AuthenticationFailed('User not found.')

        return user

    def get_queryset(self):
        user = self.request.user

        if not user:
            raise AuthenticationFailed('Unauthenticated user.')

        return Orders.objects.filter(user=user)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    


#=========================OrderDetailViewSet=============================

class OrderDetailViewSet(generics.RetrieveUpdateDestroyAPIView):
    queryset = Orders.objects.all()
    serializer_class = OrderSerializer
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method in ['PATCH', 'DELETE']:
            print(f"Request method: {self.request.method}, User: {self.request.user}, is_staff: {self.request.user.is_staff}, is_superuser: {self.request.user.is_superuser}")
            return [IsAdminUser()]
        return [IsAuthenticated()]




class OrderUpdateView(generics.UpdateAPIView):
    queryset = Orders.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        data = request.data.copy()
        
        # Ensure that total_amount and grand_total are not reset
        data.pop('total_amount', None)
        data.pop('grand_total', None)
        
        serializer = self.get_serializer(instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

    def perform_update(self, serializer):
        # If you need to perform any additional logic, you can do so here
        serializer.save()


#=========================OrderItemViewSet=============================

class OrderItemViewSet(generics.ListAPIView):
    serializer_class = OrderItemSerializer
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        order_id = self.kwargs.get('pk')
        if order_id:
            return OrderItem.objects.filter(order_id=order_id)
        return OrderItem.objects.none()
    







