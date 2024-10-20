from rest_framework import generics, status
from rest_framework.response import Response
from .models import Review, Wishlist, Compare
from store.models import Products
from .serializers import ReviewSerializer, WishlistSerializer, CompareSerializer
from rest_framework.permissions import IsAuthenticated
from accounts.token_authentication import CustomTokenAuthentication

# =====================================Review=========================
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


# ==================================WishList======================
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


# =====================================Compare====================
class CompareListView(generics.ListAPIView):
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CompareSerializer


    def get_queryset(self):
        return Compare.objects.filter(user=self.request.user)

class AddToCompareView(generics.GenericAPIView):
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CompareSerializer

    def post(self, request, *args, **kwargs):
        user = request.user
        product_ids = [item['product_id'] for item in request.data.get('products', [])]

        compare, created = Compare.objects.get_or_create(user=user)
        not_found_products = []

        for product_id in product_ids:
            try:
                product = Products.objects.get(product_id=product_id)
                compare.products.add(product)
            except Products.DoesNotExist:
                not_found_products.append(product_id)

        compare.save()

        if not_found_products:
            return Response({
                'message': 'Some products were added to comparison list.',
                'not_found_products': not_found_products
            }, status=status.HTTP_207_MULTI_STATUS)



        return Response({'message': 'Product added to comparison list.'}, status=status.HTTP_200_OK)

class RemoveFromCompareView(generics.GenericAPIView):
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CompareSerializer

   
    def post(self, request, *args, **kwargs):
        user = request.user
        product_ids = [item['product_id'] for item in request.data.get('products', [])]

        compare = Compare.objects.get(user=user)
        not_found_products = []

        for product_id in product_ids:
            try:
                product = Products.objects.get(product_id=product_id)
                compare.products.remove(product)
            except Products.DoesNotExist:
                not_found_products.append(product_id)

        compare.save()

        if not_found_products:
            return Response({
                'message': 'Some products were removed from comparison list.',
                'not_found_products': not_found_products
            }, status=status.HTTP_207_MULTI_STATUS)

        return Response({'message': 'All products removed from comparison list.'}, status=status.HTTP_200_OK)

