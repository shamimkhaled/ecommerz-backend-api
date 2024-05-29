from rest_framework import generics
from .models import Review, Wishlist
from .serializers import ReviewSerializer, WishlistSerializer
from rest_framework.permissions import IsAuthenticated
from accounts.token_authentication import CustomTokenAuthentication


class ReviewListCreate(generics.ListCreateAPIView):
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

class WishlistListCreate(generics.ListCreateAPIView):
    authentication_classes = [CustomTokenAuthentication]

    permission_classes = [IsAuthenticated]
    queryset = Wishlist.objects.all()
    serializer_class = WishlistSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class WishlistDetail(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Wishlist.objects.all()
    serializer_class = WishlistSerializer
