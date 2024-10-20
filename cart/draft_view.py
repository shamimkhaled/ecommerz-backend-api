



from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Carts, CartItem
from .serializers import CartSerializer, CartItemSerializer
from django.contrib.auth import get_user_model
from rest_framework.authentication import TokenAuthentication
# from .notifications import SendNotification  # Import your notification function

User = get_user_model()

class CartListCreateAPIView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        carts = Carts.objects.filter(user=request.user)
        serializer = CartSerializer(carts, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data.copy()
        data['user'] = str(request.user.user_id)
        serializer = CartSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CartDetailAPIView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user):
        try:
            return Carts.objects.get(cart_id=pk, user=user)
        except Carts.DoesNotExist:
            return None

    def get(self, request, pk):
        cart = self.get_object(pk, request.user)
        if not cart:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    def put(self, request, pk):
        cart = self.get_object(pk, request.user)
        if not cart:
            return Response(status=status.HTTP_404_NOT_FOUND)
        data = request.data.copy()
        data['user'] = request.user.user_id
        serializer = CartSerializer(cart, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        cart = self.get_object(pk, request.user)
        if not cart:
            return Response(status=status.HTTP_404_NOT_FOUND)
        cart.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CartItemListCreateAPIView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart_items = CartItem.objects.filter(cart__user=request.user)
        serializer = CartItemSerializer(cart_items, many=True)
        return Response(serializer.data)

    def post(self, request):
        cart_id = request.data.get('cart')
        if not cart_id:
            return Response({'error': 'Cart ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            cart = Carts.objects.get(cart_id=cart_id, user=request.user)
        except Carts.DoesNotExist:
            return Response({'error': 'Cart not found'}, status=status.HTTP_404_NOT_FOUND)
        data = request.data.copy()
        data['cart'] = str(cart.cart_id)
        serializer = CartItemSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            # Trigger the notification after saving the item
            # SendNotification(f"Item added to cart: {serializer.data['product']}", request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CartItemDetailAPIView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user):
        try:
            return CartItem.objects.get(id=pk, cart__user=user)
        except CartItem.DoesNotExist:
            return None

    def get(self, request, pk):
        cart_item = self.get_object(pk, request.user)
        if not cart_item:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = CartItemSerializer(cart_item)
        return Response(serializer.data)

    def put(self, request, pk):
        cart_item = self.get_object(pk, request.user)
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
        cart_item = self.get_object(pk, request.user)
        if not cart_item:
            return Response(status=status.HTTP_404_NOT_FOUND)
        cart_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
