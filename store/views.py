from django.shortcuts import render, get_object_or_404
# from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework import status
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from .models import *
from .serializers import *
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .filters import ProductFilters
from rest_framework import generics
from django.urls import reverse





# Create your views here.


# class CategoryViewSet(ModelViewSet):
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer


# class ProductsViewSet(ModelViewSet):
#     queryset = Products.objects.all()
#     serializer_class = ProductSerializer

# class ProductListView(generics.ListAPIView):
#     queryset = Products.objects.all()
#     serializer_class = ProductSerializer
#     filter_backends = [DjangoFilterBackend]
#     filterset_class = ProductFilters


# ========================CategoriesAPIView===============================


class ProductsAPIView(APIView):
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilters
    search_fields = ['product_title', 'short_description', 'description']
    ordering_fields = ['price', 'created_at']
    pagination_class = PageNumberPagination


    def get(self, request):
        queryset = Products.objects.all()
         #  filters
        filterset = self.filterset_class(request.GET, queryset=queryset)
        if filterset.is_valid():
            queryset = filterset.qs

        #  search
        search = request.GET.get('search', None)
        if search:
            search_filter = SearchFilter()
            queryset = search_filter.filter_queryset(request, queryset, self)

        # ordering/sorting
        ordering = request.GET.get('ordering', None)
        if ordering:
            ordering_filter = OrderingFilter()
            queryset = ordering_filter.filter_queryset(request, queryset, self)


        # Paginate Page
        paginator = self.pagination_class()
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        
        serializers = ProductSerializer(paginated_queryset, many=True)

        return Response(serializers.data)
    
    def post(self, request):
        serializers = ProductSerializer(data=request.data)
        serializers.is_valid(raise_exception=True)
        serializers.save()
        return Response(serializers.data)


    
class SingleProductAPIView(APIView):

    def get(self, request, slug):
        product = get_object_or_404(Products, slug=slug)
        serializers = ProductSerializer(product)
        return Response(serializers.data)
    
    def put(self, request, slug):
            product = get_object_or_404(Products, slug=slug)
            serializers = ProductSerializer(product, data=request.data)
            serializers.is_valid(raise_exception=True)
            serializers.save()
            return Response(serializers.data)


    def delete(self, request, slug):
                 product = get_object_or_404(Products, slug=slug)
                 product.delete()
                 return Response(status=status.HTTP_204_NO_CONTENT)
    
# class SingleProductAPIView(APIView):

#     def get(self, request, pk):
#         product = get_object_or_404(Products, product_id=pk)
#         serializers = ProductSerializer(product)
#         return Response(serializers.data)
    
#     def put(self, request, pk):
#             product = get_object_or_404(Products, product_id=pk)
#             serializers = ProductSerializer(product, data=request.data)
#             serializers.is_valid(raise_exception=True)
#             serializers.save()
            #   return Response(serializers.data)

#     def delete(self, request, pk):
#                  product = get_object_or_404(Products, product_id=pk)
#                  product.delete()
#                  return Response(status=status.HTTP_204_NO_CONTENT)


# ========================CategoriesAPIView===============================

class CategoriesAPIView(APIView):

    def get(self, request):
          categories = Category.objects.all()
          serializers = CategorySerializer(categories, many=True)
          return Response(serializers.data)
    
    def post(self, request):
        serializers = CategorySerializer(data=request.data)
        serializers.is_valid(raise_exception=True)
        serializers.save()
        return Response(serializers.data)

class SingleCategoryAPIView(APIView):

    def get(self, request, slug):
        category = get_object_or_404(Category, slug=slug)
        serializer = CategorySerializer(category)
        return Response(serializer.data)
    
    def put(self, request, slug):
         category = get_object_or_404(Category, slug=slug)
         serializers = CategorySerializer(category, data=request.data)
         serializers.is_valid(raise_exception=True)
         serializers.save()
         return Response(serializers.data)
    
    def delete(self, request, slug):
            category = get_object_or_404(Category, slug=slug)
            category.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
    
         
# ========================ProductVariationView===============================


class ProductVariationCategoryAPIView(APIView):

    def get(self, request):
          variation_category = ProductVariationCategory.objects.all()
          serializers = VariationCategorySerializer(variation_category, many=True)
          return Response(serializers.data)
    
    def post(self, request):
        serializers = VariationCategorySerializer(data=request.data)
        serializers.is_valid(raise_exception=True)
        serializers.save()
        return Response(serializers.data)
    

class ProductVariationAPIView(APIView):

    def get(self, request):
          variation = ProductVariation.objects.all()
          serializers = ProductVaraiationSerializer(variation, many=True)
          return Response(serializers.data)
    
    def post(self, request):
        serializers = ProductVaraiationSerializer(data=request.data)
        serializers.is_valid(raise_exception=True)
        serializers.save()
        return Response(serializers.data)


class SingleProductVariationValueAPI(APIView):
     
    def get(self, request, pk):
        variation = get_object_or_404(ProductVariation, variation_id=pk)
        serializers = ProductVaraiationSerializer(variation)
        return Response(serializers.data)
    
    def put(self, request, pk):
            variation = get_object_or_404(ProductVariation, variation_id=pk)
            serializers = ProductVaraiationSerializer(variation, data=request.data)
            serializers.is_valid(raise_exception=True)
            serializers.save()
            return Response(serializers.data)


    def delete(self, request, pk):
                 variation = get_object_or_404(ProductVariation, variation_id=pk)
                 variation.delete()
                 return Response(status=status.HTTP_204_NO_CONTENT)
    




 
    