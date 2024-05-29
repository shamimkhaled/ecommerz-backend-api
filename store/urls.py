from .views import *
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework import routers


# router = routers.DefaultRouter()

# router.register("products", views.ProductsViewSet)
# router.register("categories", views.CategoryViewSet)


urlpatterns = [
    # path('product', ProductListView.as_view()),
    path('products/', ProductsAPIView.as_view()),

    path('products/<slug:slug>', SingleProductAPIView.as_view()),
    # path('products/<str:pk>', SingleProductAPIView.as_view()),
    path('categories/', CategoriesAPIView.as_view()),
    path('categories/<slug:slug>', SingleCategoryAPIView.as_view()),
    path('variation-categories/', ProductVariationCategoryAPIView.as_view()),
    path('variation-value/', ProductVariationAPIView.as_view()),
    path('variation-value/<str:pk>', SingleProductVariationValueAPI.as_view())

]