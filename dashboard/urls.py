from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ( DashboardIndexView, ProductListView, CategoryListView,
                     AddNewProduct, UpdateProductView, ProductDeleteView,
                    AddNewCategory, UpdateCategoryView, CategoryDeleteView,
                    ProductVariationListView, ProductVariationCategoryListView,
                    AddNewVariationCategory, UpdateVariationCategoryView, VariationCategoryDeleteView,
                    AddNewProductVariation, UpdateProductVariationView,
                    ProductVariationDeleteView, CartListView, CartItemListView,
                    CreateNewCartView, UpdateCartView,CartDeleteView,
                    AddNewCartItemView, UpdateCartItemView, CartItemDeleteView,
                    CouponCodeListView, CreateNewCouponCodeView, UpdateCouponCodeView,
                    CouponCodeDeleteView, OrderListView, CreateNewOrderView, UpdateOrderView,
                    OrderDeleteView, OrderItemDeleteView, OrderItemListView,
                    CreateNewOrderItemView, UpdateOrderItemView, ShippingListView,
                    ShippingDeleteView, CreateShippingView, UpdateShippingView,
                    PaymentDeleteView, CreatePaymentView, PaymentListView, UpdatePaymentView,
                    ReviewListView, ReviewDeleteView, CreateReviewView,
                    UpdateReviewView, CompareListView, CreateCompareView,
                    UpdateCompareView, CompareDeleteView, WishlistListView,
                    CreateWishlistView, UpdateWishlistView, WishlistDeleteView,
                    UserListView,


)                  



app_name = 'dashboard'  

urlpatterns = [

    # path('accounts/', include('accounts.urls')),
    path('', DashboardIndexView.as_view(), name='dashboard'),
    path('products/', ProductListView.as_view(), name='product'),
    path('product/add-product/', AddNewProduct.as_view(), name='add_product'),
    path('product/edit-product/<slug:slug>/', UpdateProductView.as_view(), name='edit_product'),
    path('delete-product/<slug:slug>/', ProductDeleteView.as_view(), name='delete_product'),


    path('category/', CategoryListView.as_view(), name='category'),
    path('category/add-category/', AddNewCategory.as_view(), name='add_category'),
    path('category/edit-category/<slug:slug>/', UpdateCategoryView.as_view(), name='edit_category'),
    path('category/delete-category/<slug:slug>/', CategoryDeleteView.as_view(), name='delete_category'),


    path('product/variation-categories/', ProductVariationCategoryListView.as_view(), name='variation_categories'),
    path('product/add-variation-category/', AddNewVariationCategory.as_view(), name='add_variation_category'),
    path('product/edit-variation-category/<int:id>/', UpdateVariationCategoryView.as_view(), name='edit_variation_category'),
    path('product/delete-variation-category/<int:id>/', VariationCategoryDeleteView.as_view(), name='delete_variation_category'),
 

    path('product/variations/', ProductVariationListView.as_view(), name='product_variation'),
    path('product/add-variation/', AddNewProductVariation.as_view(), name='add_product_variation'),
    path('product/edit-variation/<uuid:pk>', UpdateProductVariationView.as_view(), name='edit_product_variation'),
    path('product/delete-variation/<uuid:pk>', ProductVariationDeleteView.as_view(), name='delete_product_variation'),



    path('cart/', CartListView.as_view(), name='cart'),
    path('create-cart/', CreateNewCartView.as_view(), name='create_cart'),
    path('update-cart/<uuid:pk>/', UpdateCartView.as_view(), name='update_cart'),
    path('delete-cart/<uuid:pk>/', CartDeleteView.as_view(), name='delete_cart'),




    path('cart-items/', CartItemListView.as_view(), name="cart_items"),
    path('add-cart-items/', AddNewCartItemView.as_view(), name="add_cart_items"),
    path('update-cart-items/<int:pk>/', UpdateCartItemView.as_view(), name="update_cart_items"),
    path('delete-cart-items/<int:pk>/', CartItemDeleteView.as_view(), name="delete_cart_items"),




    path('coupon-codes/', CouponCodeListView.as_view(), name="coupon_code"),
    path('create-coupon-codes/', CreateNewCouponCodeView.as_view(), name="create_coupon_code"),
    path('update-coupon-codes/<int:pk>/', UpdateCouponCodeView.as_view(), name="update_coupon_code"),
    path('delete-coupon-codes/<int:pk>/', CouponCodeDeleteView.as_view(), name="delete_coupon_code"),


    path('order/', OrderListView.as_view(), name="order"),
    path('order/create-order/', CreateNewOrderView.as_view(), name="create_order"),
    path('order/update-order/<uuid:pk>/', UpdateOrderView.as_view(), name="update_order"),
    path('order/delete-order/<uuid:pk>/', OrderDeleteView.as_view(), name="delete_order"),



    path('order-items/', OrderItemListView.as_view(), name="order_item"),
    path('order-item/create-order-item/', CreateNewOrderItemView.as_view(), name="create_order_item"),
    path('order-item/update-order-item/<int:pk>/', UpdateOrderItemView.as_view(), name="update_order_item"),
    path('order-item/delete-order-item/<int:pk>/', OrderItemDeleteView.as_view(), name="delete_order_item"),



    path('shipping-list/', ShippingListView.as_view(), name="shipping"),
    path('create-shipping/', CreateShippingView.as_view(), name="create_shipping"),
    path('update-shipping/<int:pk>/', UpdateShippingView.as_view(), name="update_shipping"),
    path('delete-shipping/<int:pk>/', ShippingDeleteView.as_view(), name="delete_shipping"),

    
    path('payments/', PaymentListView.as_view(), name="payment"),
    path('payments/create-payment/', CreatePaymentView.as_view(), name="create_payment"),
    path('payments/update-payment/<int:pk>/', UpdatePaymentView.as_view(), name="update_payment"),
    path('payments/delete-payment/<int:pk>/', PaymentDeleteView.as_view(), name="delete_payment"),



    path('reviews/', ReviewListView.as_view(), name="review"),
    path('reviews/create-review/', CreateReviewView.as_view(), name="create_review"),
    path('reviews/update-review/<int:pk>/', UpdateReviewView.as_view(), name="update_review"),
    path('reviews/delete-review/<int:pk>', ReviewDeleteView.as_view(), name="delete_review"),
    
    
    path('compare/', CompareListView.as_view(), name="compare"),
    path('compare/create-compare/', CreateCompareView.as_view(), name="create_compare"),
    path('compare/update-compare/<int:pk>/', UpdateCompareView.as_view(), name="update_compare"),
    path('compare/delete-compare/<int:pk>', CompareDeleteView.as_view(), name="delete_compare"),

    path('wishlists/', WishlistListView.as_view(), name="wishlist"),
    path('wishlist/create-wishlist/', CreateWishlistView.as_view(), name="create_wishlist"),
    path('wishlist/update-wishlist/<int:pk>/', UpdateWishlistView.as_view(), name="update_wishlist"),
    path('wishlist/delete-wishlist/<int:pk>', WishlistDeleteView.as_view(), name="delete_wishlist"),


    path('users/', UserListView.as_view(), name="user"),






    







]