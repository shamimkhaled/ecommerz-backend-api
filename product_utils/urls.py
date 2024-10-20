from django.urls import path
from .views import (ReviewListCreate, ReviewDetail,
                     WishlistListCreate, WishlistDetail,
                     CompareListView, AddToCompareView,
                     RemoveFromCompareView)

urlpatterns = [
    path('product/reviews/', ReviewListCreate.as_view(), name='review-list-create'),
    path('product/reviews/<int:pk>/', ReviewDetail.as_view(), name='review-detail'),
    path('product/wishlists/', WishlistListCreate.as_view(), name='wishlist-list-create'),
    path('product/wishlists/<int:pk>/', WishlistDetail.as_view(), name='wishlist-detail'),
    path('compare/', CompareListView.as_view(), name='compare-list'),
    path('compare/add/', AddToCompareView.as_view(), name='add-to-compare'),
    path('compare/remove/', RemoveFromCompareView.as_view(), name='remove-from-compare'),
]
