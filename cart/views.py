
# from notification.notific import SendNotification
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Carts, CartItem
from accounts.models import UserAccount
from .serializers import CartSerializer, CartItemSerializer, AddCartItemSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth import get_user_model
from django.conf import settings
import jwt
from couponcode.models import Coupon
from couponcode.serializers import CouponSerializer, ApplyCouponSerializers
from django.utils import timezone
from accounts.token_authentication import CustomTokenAuthentication





class CartListCreateAPIView(APIView):
    authentication_classes = [TokenAuthentication]

    permission_classes = (AllowAny,)

    def get(self, request):
        user_token = request.COOKIES.get('access_token')

        if not user_token:
            raise AuthenticationFailed('Unauthenticated user.')

        payload = jwt.decode(user_token, settings.SECRET_KEY, algorithms=['HS256'])

        model = get_user_model()
        user = model.objects.filter(user_id=payload['user_id']).first()
        
        carts = Carts.objects.filter(user=user)
        serializer = CartSerializer(carts, many=True)
        return Response(serializer.data)

    def post(self, request):
        user_token = request.COOKIES.get('access_token')

        if not user_token:
            return Response({'error': 'Authentication required to create a cart'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            payload = jwt.decode(user_token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return Response({'error': 'Token has expired'}, status=status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidTokenError:
            return Response({'error': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)

        model = get_user_model()
        user = model.objects.filter(user_id=payload['user_id']).first()
        
        if not user:
            return Response({'error': 'User not found'}, status=status.HTTP_401_UNAUTHORIZED)

        data = request.data.copy()
        data['user'] = str(user.user_id)
        serializer = CartSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

   
    

class CartDetailAPIView(APIView):
    authentication_classes = [TokenAuthentication]

    permission_classes = [AllowAny]

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

    def get_object(self, pk, user):
        try:
            return Carts.objects.get(cart_id=pk, user=user)
        except Carts.DoesNotExist:
            return None

    def get(self, request, pk):
        user = self.get_user_from_token(request)
        cart = self.get_object(pk, user)
        if not cart:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    def put(self, request, pk):
        user = self.get_user_from_token(request)
        cart = self.get_object(pk, user)
        if not cart:
            return Response(status=status.HTTP_404_NOT_FOUND)
        data = request.data.copy()
        data['user'] = str(user.user_id)
        serializer = CartSerializer(cart, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user = self.get_user_from_token(request)
        cart = self.get_object(pk, user)
        if not cart:
            return Response(status=status.HTTP_404_NOT_FOUND)
        cart.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class CartItemListCreateAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]

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
        return CartItem.objects.filter(cart_id=self.kwargs["cart_pk"])
    
    def get_serializer_class(self):
        if self.request.method == "POST":
            return AddCartItemSerializer
        return CartItemSerializer
    
    def get_serializer_context(self, cart_id):
        return {"cart_id": cart_id}

    def get(self, request):
        user = self.get_user_from_token(request)
        cart_items = CartItem.objects.filter(cart__user=user)
        serializer = CartItemSerializer(cart_items, many=True)
        return Response(serializer.data)

    def post(self, request):
        # user = self.get_user_from_token(request)
        # cart_id = request.data.get('cart')
        # if not cart_id:
        #     return Response({'error': 'Cart ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        # try:
        #     cart = Carts.objects.get(cart_id=cart_id, user=user)
        # except Carts.DoesNotExist:
        #     return Response({'error': 'Cart not found'}, status=status.HTTP_404_NOT_FOUND)
        # data = request.data.copy()
        # data['cart'] = cart.cart_id
        # serializer_class = self.get_serializer_class()
        # serializer = serializer_class(data=data, context=self.get_serializer_context)

        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(serializer.data, status=status.HTTP_201_CREATED)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = self.get_user_from_token(request)
        cart_id = request.data.get('cart')
        if not cart_id:
            return Response({'error': 'Cart ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
           cart =  Carts.objects.get(cart_id=cart_id, user=user)
        except Carts.DoesNotExist:
            return Response({'error': 'Cart not found'}, status=status.HTTP_404_NOT_FOUND)
        data = request.data.copy()
        data['cart'] = cart.cart_id
        serializer_class = self.get_serializer_class()
        serializer_context = self.get_serializer_context(cart_id=cart_id)
        serializer = serializer_class(data=data, context=serializer_context)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class CartItemDetailAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]

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

    def get_object(self, pk, user):
        try:
            return CartItem.objects.get(id=pk, cart__user=user)
        except CartItem.DoesNotExist:
            return None

    def get(self, request, pk):
        user = self.get_user_from_token(request)
        cart_item = self.get_object(pk, user)
        if not cart_item:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = CartItemSerializer(cart_item)
        return Response(serializer.data)

    def put(self, request, pk):
        user = self.get_user_from_token(request)
        cart_item = self.get_object(pk, user)
        if not cart_item:
            return Response(status=status.HTTP_404_NOT_FOUND)
        data = request.data.copy()
        data['cart'] = str(cart_item.cart.cart_id)
        serializer = CartItemSerializer(cart_item, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user = self.get_user_from_token(request)
        cart_item = self.get_object(pk, user)
        if not cart_item:
            return Response(status=status.HTTP_404_NOT_FOUND)
        cart_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)





# class ApplyCouponCodeView(generics.GenericAPIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [AllowAny]
#     serializer_class = CartSerializer

#     def get_user_from_token(self, request):
#         user_token = request.COOKIES.get('access_token')
#         if not user_token:
#             raise AuthenticationFailed('Unauthenticated user.')

#         try:
#             payload = jwt.decode(user_token, settings.SECRET_KEY, algorithms=['HS256'])
#         except jwt.ExpiredSignatureError:
#             raise AuthenticationFailed('Token has expired.')
#         except jwt.InvalidTokenError:
#             raise AuthenticationFailed('Invalid token.')

#         model = get_user_model()
#         user = model.objects.filter(pk=payload['user_id']).first()
        
#         if not user:
#             raise AuthenticationFailed('User not found.')

#         return user

#     def put(self, request, cart_id):
#         user = self.get_user_from_token(request)
        
#         try:
#             cart = Carts.objects.get(cart_id=cart_id, user=user)
#         except Carts.DoesNotExist:
#             return Response({"error": "Cart not found."}, status=status.HTTP_404_NOT_FOUND)

#         if cart.user != user:
#             return Response({"error": "This cart does not belong to you."}, status=status.HTTP_403_FORBIDDEN)

#         coupon_code = request.data.get('coupon_code', '')

#         if not coupon_code:
#             return Response({"error": "Coupon code is required"}, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             coupon = Coupon.objects.get(code=coupon_code, active=True)
#             if not (coupon.valid_from <= timezone.now() <= coupon.valid_to):
#                 return Response({"error": "Coupon is not valid at this time"}, status=status.HTTP_400_BAD_REQUEST)
#         except Coupon.DoesNotExist:
#             return Response({"error": "Invalid coupon code"}, status=status.HTTP_400_BAD_REQUEST)

#         # Apply the coupon to the cart
#         cart.coupon = coupon
#         cart.save()

#         # Calculate the new total price with the coupon applied
#         total_price = sum(item.sub_total() for item in cart.cartitems.all())
#         discount = (total_price * coupon.discount) / 100
#         total_price -= discount

#         # Serialize and return the updated cart data
#         serializer = self.get_serializer(cart)
#         cart_data = serializer.data
#         cart_data['total_price'] = total_price  # Overwrite the total price with the discounted price

#         return Response(cart_data, status=status.HTTP_200_OK)


class ApplyCouponCodeView(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]
    serializer_class = ApplyCouponSerializers

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

    def post(self, request, cart_id):
        user = self.get_user_from_token(request)
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            coupon_code = serializer.validated_data['coupon_code']

            try:
                coupon = Coupon.objects.get(code=coupon_code, active=True, valid_from__lte=timezone.now(), valid_to__gte=timezone.now())
            except Coupon.DoesNotExist:
                return Response({'error': 'Coupon code is not valid'}, status=status.HTTP_404_NOT_FOUND)

            try:
                cart = Carts.objects.get(cart_id=cart_id, user=user)
                if cart.coupon == coupon:
                    return Response({'message': 'This coupon code is already applied to your cart.'}, status=status.HTTP_200_OK)
                
                cart.apply_coupon(coupon)
                cart.save()
            except Carts.DoesNotExist:
                return Response({'error': 'Cart not found'}, status=status.HTTP_404_NOT_FOUND)

            return Response({'message': 'Coupon applied successfully'}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)