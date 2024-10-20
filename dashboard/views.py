# import imp
from django.shortcuts import redirect, render

from django.views.generic import TemplateView, ListView
from django.views.generic.edit import DeleteView
from store.models import Products, Category, ProductVariation, ProductVariationCategory
from store.forms import ProductsForm, CategoryForm, VariationCategoryForm, ProductVariationForm
from cart.models import Carts, CartItem
from cart.forms import CartForm, CartItemForm
from couponcode.models import Coupon
from couponcode.forms import CouponCodeForm
from order.models import OrderItem, Orders, Shipping
from order.forms import OrderForm, OrderItemForm, ShippingForm
from payment.models import Payment, BillingAddress
from payment.forms import PaymentForm, BillingAddressForm
from accounts.models import UserAccount, UserProfile
from product_utils.models import Compare, Wishlist, Review
from product_utils.forms import ReviewForm, CompareForm, WishlistForm
from django.utils.text import slugify
from django.http import JsonResponse



# Create your views here.

# this is for dashboard index
class DashboardIndexView(TemplateView):
    def get(self, request, *args, **kwargs):
        return render(request, 'admin/dashboard.html')


    def post(self, request, *args, **kwargs):
        pass


#==========================================ProductAllView======================================
class ProductListView(TemplateView):
    def get(self, request, *args, **kwargs):
        products = Products.objects.all().order_by('-created_at')
        context = {
            'products': products
        }
        return render(request, 'admin/store/product.html', context)


    def post(self, request, *args, **kwargs):
        pass


# Add Product
class AddNewProduct(TemplateView):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_staff or request.user.is_admin or request.user.is_superuser:
                form = ProductsForm()
                context = {
                    'form': form
                }
                return render(request, 'admin/store/add_product.html', context)
            else:
                return redirect('store:products')
        else:
            return redirect('store:products')

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated and (request.user.is_staff or request.user.is_admin or request.user.is_superuser):
            form = ProductsForm(request.POST, request.FILES)
            if form.is_valid():
                product = form.save(commit=False)
                product.slug = slugify(product.product_title)
                product.save()
                return redirect('dashboard:product')
            else:
                categories = Category.objects.all()
                context = {
                    'form': form,
                    'categories': categories
                }
                return render(request, self.template_name, context)
        else:
            return redirect('store:products')


#==========================================UpdateProductView======================================

class UpdateProductView(TemplateView):
    # template_name = 'admin/store/edit_product.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated and (request.user.is_staff or request.user.is_admin or request.user.is_superuser):
            products = Products.objects.get(slug=kwargs['slug'])
            form = ProductsForm(instance=products)
            context = {
                'form': form,
                'products': products
            }
            return render(request, 'admin/store/edit_product.html', context)
        else:
            return redirect('store:products')

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated and (request.user.is_staff or request.user.is_admin or request.user.is_superuser):
            slug = kwargs.get('slug')
            products = Products.objects.get(slug=slug)
            form = ProductsForm(request.POST, request.FILES, instance=products)
            if form.is_valid():
                product = form.save(commit=False)
                product.slug = slugify(product.product_title)
                product.save()
                return redirect('dashboard:product')
            else:
                context = {
                    'form': form,
                    'products': products
                }
                return render(request, 'admin/store/edit_product.html', context)
        else:
            return redirect('store:products')





class ProductDeleteView(TemplateView):
    def get(self, request, slug, *args, **kwargs):
        if request.user.is_authenticated and (request.user.is_staff or request.user.is_admin or request.user.is_superuser):
            products = Products.objects.get(slug=slug)
            products.delete()
            return redirect('dashboard:product')


#==========================================CategoryAllView======================================
class CategoryListView(TemplateView):
    def get(self, request, *args, **kwargs):
        categories = Category.objects.all().order_by('-created_at')
        context = {
            'categories': categories
        }
        return render(request, 'admin/store/category.html', context)


    def post(self, request, *args, **kwargs):
        pass



class AddNewCategory(TemplateView):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_staff or request.user.is_admin or request.user.is_superuser:
                form = CategoryForm()
                context = {
                    'form': form
                }
                return render(request, 'admin/store/add_category.html', context)
            else:
                return redirect('store:products')
        else:
            return redirect('store:products')

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated and (request.user.is_staff or request.user.is_admin or request.user.is_superuser):
            form = CategoryForm(request.POST, request.FILES)
            if form.is_valid():
                category = form.save(commit=False)
                category.slug = slugify(category.slug)
                category.save()
                return redirect('dashboard:category')
            else:
                categories = Category.objects.all()
                context = {
                    'form': form,
                    'categories': categories
                }
                return render(request, 'admin/store/add_category.html', context)
        else:
            return redirect('store:products')




# class UpdateCategoryView(TemplateView):
#     # template_name = 'admin/store/edit_product.html'

#     def get(self, request, *args, **kwargs):
#         if request.user.is_authenticated and (request.user.is_staff or request.user.is_admin or request.user.is_superuser):
#             categories = Category.objects.get(slug=kwargs['slug'])
#             form = CategoryForm(instance=categories)
#             context = {
#                 'form': form,
#                 'categories': categories
#             }
#             return render(request, 'admin/store/edit_category.html', context)
#         else:
#             return redirect('store:index')

#     def post(self, request, *args, **kwargs):
#         if request.user.is_authenticated and (request.user.is_staff or request.user.is_admin or request.user.is_superuser):
#             slug = kwargs.get('slug')
#             categories = Category.objects.get(slug=slug)
#             form = CategoryForm(request.POST, request.FILES, instance=categories)
#             if form.is_valid():
#                 category = form.save(commit=False)
#                 category.slug = slugify(category.category_title)
#                 category.save()
#                 return redirect('dashboard:category')
#             else:
#                 context = {
#                     'form': form,
#                     'categories': categories
#                 }
#                 return render(request, 'admin/store/edit_category.html', context)
#         else:
#             return redirect('store:index')


class UpdateCategoryView(TemplateView):
    template_name = 'admin/store/edit_category.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated and (request.user.is_staff or request.user.is_admin or request.user.is_superuser):
            category = Category.objects.get(slug=kwargs['slug'])
            form = CategoryForm(instance=category)
            context = {
                'form': form,
                'category': category
            }
            return render(request, self.template_name, context)
        else:
            return redirect('store:products')

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated and (request.user.is_staff or request.user.is_admin or request.user.is_superuser):
            slug = kwargs.get('slug')
            category = Category.objects.get(slug=slug)
            form = CategoryForm(request.POST, request.FILES, instance=category)
            if form.is_valid():
                category = form.save(commit=False)
                category.slug = slugify(category.category_title)
                category.save()
                return redirect('dashboard:category')
            else:
                context = {
                    'form': form,
                    'category': category
                }
                return render(request, self.template_name, context)
        else:
            return redirect('store:products')
        

class CategoryDeleteView(TemplateView):
    def get(self, request, slug, *args, **kwargs):
        if request.user.is_authenticated and (request.user.is_staff or request.user.is_admin or request.user.is_superuser):
            category = Category.objects.get(slug=slug)
            category.delete()
            return redirect('dashboard:category')



#==========================================ProductVariationCategoryAllView======================================
class ProductVariationCategoryListView(TemplateView):
    def get(self, request, *args, **kwargs):
        variation_category = ProductVariationCategory.objects.all().order_by('-created_at')
        context = {
            'variation_category': variation_category
        }
        return render(request, 'admin/store/product_variation_category.html', context)


    def post(self, request, *args, **kwargs):
        pass


class AddNewVariationCategory(TemplateView):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_staff or request.user.is_admin or request.user.is_superuser:
                form = VariationCategoryForm()
                context = {
                    'form': form
                }
                return render(request, 'admin/store/add_variation_category.html', context)
            else:
                return redirect('store:products')
        else:
            return redirect('store:products')

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated and (request.user.is_staff or request.user.is_admin or request.user.is_superuser):
            form = VariationCategoryForm(request.POST, request.FILES)
            if form.is_valid():
                variation_category = form.save(commit=False)
                # variation_category.id = slugify(variation_category.id)
                variation_category.save()
                return redirect('dashboard:variation_categories')
            else:
                variation_categories = ProductVariationCategory.objects.all()
                context = {
                    'form': form,
                    'categories': variation_categories
                }
                return render(request, 'admin/store/add_variation_category.html', context)
        else:
            return redirect('store:products')




class UpdateVariationCategoryView(TemplateView):
    template_name = 'admin/store/edit_product_variation_category.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated and (request.user.is_staff or request.user.is_admin or request.user.is_superuser):
            category = ProductVariationCategory.objects.get(id=kwargs['id'])
            form = VariationCategoryForm(instance=category)
            context = {
                'form': form,
                'category': category
            }
            return render(request, self.template_name, context)
        else:
            return redirect('store:products')

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated and (request.user.is_staff or request.user.is_admin or request.user.is_superuser):
            id = kwargs.get('id')
            category = ProductVariationCategory.objects.get(id=id)
            form = VariationCategoryForm(request.POST, request.FILES, instance=category)
            if form.is_valid():
                category = form.save(commit=False)
                category.id = category.id
                category.save()
                return redirect('dashboard:variation_categories')
            else:
                context = {
                    'form': form,
                    'category': category
                }
                return render(request, self.template_name, context)
        else:
            return redirect('store:products')
        

class VariationCategoryDeleteView(TemplateView):
    def get(self, request, id, *args, **kwargs):
        if request.user.is_authenticated and (request.user.is_staff or request.user.is_admin or request.user.is_superuser):
            category = ProductVariationCategory.objects.get(id=id)
            category.delete()
            return redirect('dashboard:variation_categories')




#==========================================ProductVariationCategoryAllView======================================


class ProductVariationListView(TemplateView):
    def get(self, request, *args, **kwargs):
        product_variation = ProductVariation.objects.all().order_by('-created_at')
        context = {
            'product_variation': product_variation
        }
        return render(request, 'admin/store/product_variation.html', context)


    def post(self, request, *args, **kwargs):
        pass


class AddNewProductVariation(TemplateView):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_staff or request.user.is_admin or request.user.is_superuser:
                form = ProductVariationForm()
                context = {
                    'form': form
                }
                return render(request, 'admin/store/add_product_variation.html', context)
            else:
                return redirect('store:products')
        else:
            return redirect('store:products')

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated and (request.user.is_staff or request.user.is_admin or request.user.is_superuser):
            form = ProductVariationForm(request.POST, request.FILES)
            if form.is_valid():
                variation = form.save(commit=False)
                # variation_category.id = slugify(variation_category.id)
                variation.save()
                return redirect('dashboard:product_variation')
            else:
                product_variation = ProductVariation.objects.all()
                context = {
                    'form': form,
                    'product_variation': product_variation
                }
                return render(request, 'admin/store/add_product_variation.html', context)
        else:
            return redirect('store:products')




# class UpdateProductVariationView(TemplateView):
#     template_name = 'admin/store/edit_product_variation.html'

#     def get(self, request, *args, **kwargs):
#         if request.user.is_authenticated and (request.user.is_staff or request.user.is_admin or request.user.is_superuser):
#             variation_id = kwargs.get('variation_id')
#             variation = ProductVariation.objects.get(variation_id=pk)
#             form = ProductVariationForm(instance=variation)
#             context = {
#                 'form': form,
#                 'variation': variation
#             }
#             return render(request, self.template_name, context)
#         else:
#             return redirect('store:products')

#     def post(self, request, *args, **kwargs):
#         if request.user.is_authenticated and (request.user.is_staff or request.user.is_admin or request.user.is_superuser):
#             variation_id = kwargs.get('variation_id')
#             variation = ProductVariation.objects.get(variation_id=pk)
#             form = ProductVariationForm(request.POST, request.FILES, instance=variation)
#             if form.is_valid():
#                 variation = form.save(commit=False)
#                 variation.variation_id = category.variation_id
#                 variation.save()
#                 return redirect('dashboard:product_variation')
#             else:
#                 context = {
#                     'form': form,
#                     'variation': variation
#                 }
#                 return render(request, self.template_name, context)
#         else:
#             return redirect('store:products')
        

class UpdateProductVariationView(TemplateView):
    template_name = 'admin/store/edit_product_variation.html'

    def get(self, request, pk, *args, **kwargs):
        if request.user.is_authenticated and (request.user.is_staff or request.user.is_admin or request.user.is_superuser):
            try:
                variation = ProductVariation.objects.get(pk=pk)
                form = ProductVariationForm(instance=variation)
                context = {
                    'form': form,
                    'variation': variation
                }
                return render(request, self.template_name, context)
            except ProductVariation.DoesNotExist:
                return redirect('store:products')
        else:
            return redirect('store:products')

    def post(self, request, pk, *args, **kwargs):
        if request.user.is_authenticated and (request.user.is_staff or request.user.is_admin or request.user.is_superuser):
            try:
                variation = ProductVariation.objects.get(pk=pk)
                form = ProductVariationForm(request.POST, request.FILES, instance=variation)
                if form.is_valid():
                    variation = form.save(commit=False)
                    variation.save()
                    return redirect('dashboard:product_variation')
                else:
                    context = {
                        'form': form,
                        'variation': variation
                    }
                    return render(request, self.template_name, context)
            except ProductVariation.DoesNotExist:
                return redirect('store:products')
        else:
            return redirect('store:products')

class ProductVariationDeleteView(TemplateView):
    def get(self, request, pk, *args, **kwargs):
        if request.user.is_authenticated and (request.user.is_staff or request.user.is_admin or request.user.is_superuser):
            try:
                variation = ProductVariation.objects.get(pk=pk)
                variation.delete()
            except ProductVariation.DoesNotExist:
                pass
            return redirect('dashboard:product_variation')
        else:
            return redirect('store:products')



# class ProductVariationDeleteView(TemplateView):
#     def get(self, request, variation_id, *args, **kwargs):
#         if request.user.is_authenticated and (request.user.is_staff or request.user.is_admin or request.user.is_superuser):
#             variation = ProductVariation.objects.get(variation_id=variation_id)
#             variation.delete()
#             return redirect('dashboard:product_variation')
#         else:
#             return redirect('store:products')


# =====================CartAllView=================
class CartListView(TemplateView):
    def get(self, request, *args, **kwargs):
        carts = Carts.objects.all().order_by('-created_at')
        context = {
            'carts': carts
        }
        return render(request, 'admin/cart/cart.html', context)


    def post(self, request, *args, **kwargs):
        pass


class CreateNewCartView(TemplateView):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_staff or request.user.is_admin or request.user.is_superuser:
                form = CartForm()
                context = {
                    'form': form
                }
                return render(request, 'admin/cart/create_cart.html', context)
            else:
                return redirect('store:products')
        else:
            return redirect('store:products')

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated and (request.user.is_staff or request.user.is_admin or request.user.is_superuser):
            form = CartForm(request.POST, request.FILES)
            if form.is_valid():
                cart = form.save(commit=False)
                # variation_category.id = slugify(variation_category.id)
                cart.save()
                return redirect('dashboard:cart')
            else:
                carts = Carts.objects.all()
                context = {
                    'form': form,
                    'carts': carts
                }
                return render(request, 'admin/cart/create_cart.html', context)
        else:
            return redirect('store:products')



class UpdateCartView(TemplateView):
    template_name = 'admin/cart/edit_cart.html'

    def get(self, request, pk, *args, **kwargs):
        if request.user.is_authenticated and (request.user.is_staff or request.user.is_admin or request.user.is_superuser):
            try:
                carts = Carts.objects.get(pk=pk)
                form = CartForm(instance=carts)
                context = {
                    'form': form,
                    'carts': carts
                }
                return render(request, self.template_name, context)
            except Carts.DoesNotExist:
                return redirect('store:products')
        else:
            return redirect('store:products')

    def post(self, request, pk, *args, **kwargs):
        if request.user.is_authenticated and (request.user.is_staff or request.user.is_admin or request.user.is_superuser):
            try:
                cart_id = Carts.objects.get(pk=pk)
                form = CartForm(request.POST, request.FILES, instance=cart_id)
                if form.is_valid():
                    cart = form.save(commit=False)
                    cart.save()
                    return redirect('dashboard:cart')
                else:
                    context = {
                        'form': form,
                        'cart': cart
                    }
                    return render(request, self.template_name, context)
            except Carts.DoesNotExist:
                return redirect('store:products')
        else:
            return redirect('store:products')

class CartDeleteView(TemplateView):
    def get(self, request, pk, *args, **kwargs):
        if request.user.is_authenticated and (request.user.is_staff or request.user.is_admin or request.user.is_superuser):
            try:
                carts = Carts.objects.get(pk=pk)
                carts.delete()
            except Carts.DoesNotExist:
                pass
            return redirect('dashboard:cart')
        else:
            return redirect('store:products')





# =====================CartItemAllView=================
class CartItemListView(TemplateView):
    def get(self, request, *args, **kwargs):
        cart_items = CartItem.objects.all().order_by('-created_at')
        context = {
            'cart_items': cart_items
        }
        return render(request, 'admin/cart/cart_item.html', context)


    def post(self, request, *args, **kwargs):
        pass



class AddNewCartItemView(TemplateView):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_staff or request.user.is_admin or request.user.is_superuser:
                form = CartItemForm()
                context = {
                    'form': form
                }
                return render(request, 'admin/cart/create_cart_item.html', context)
            else:
                return redirect('store:products')
        else:
            return redirect('store:products')

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated and (request.user.is_staff or request.user.is_admin or request.user.is_superuser):
            form = CartItemForm(request.POST, request.FILES)
            if form.is_valid():
                cart_item = form.save(commit=False)
                # variation_category.id = slugify(variation_category.id)
                cart_item.save()
                return redirect('dashboard:cart_items')
            else:
                cart_items = CartItem.objects.all()
                context = {
                    'form': form,
                    'cart_items': cart_items
                }
                return render(request, 'admin/cart/create_cart_item.html', context)
        else:
            return redirect('store:products')



class UpdateCartItemView(TemplateView):
    template_name = 'admin/cart/edit_cart_item.html'

    def get(self, request, pk, *args, **kwargs):
        if request.user.is_authenticated and (request.user.is_staff or request.user.is_admin or request.user.is_superuser):
            try:
                cart_items = CartItem.objects.get(pk=pk)
                form = CartItemForm(instance=cart_items)
                context = {
                    'form': form,
                    'cart_items': cart_items
                }
                return render(request, self.template_name, context)
            except CartItem.DoesNotExist:
                return redirect('store:products')
        else:
            return redirect('store:products')

    def post(self, request, pk, *args, **kwargs):
        if request.user.is_authenticated and (request.user.is_staff or request.user.is_admin or request.user.is_superuser):
            try:
                cart_id = CartItem.objects.get(pk=pk)
                form = CartItemForm(request.POST, request.FILES, instance=cart_id)
                if form.is_valid():
                    cart_item = form.save(commit=False)
                    cart_item.save()
                    return redirect('dashboard:cart_items')
                else:
                    context = {
                        'form': form,
                        'cart_item': cart_item
                    }
                    return render(request, self.template_name, context)
            except CartItem.DoesNotExist:
                return redirect('store:products')
        else:
            return redirect('store:products')

class CartItemDeleteView(TemplateView):
    def get(self, request, pk, *args, **kwargs):
        if request.user.is_authenticated and (request.user.is_staff or request.user.is_admin or request.user.is_superuser):
            try:
                cart_items = CartItem.objects.get(pk=pk)
                cart_items.delete()
            except CartItem.DoesNotExist:
                pass
            return redirect('dashboard:cart_items')
        else:
            return redirect('store:products')



# ==========================CouponCodeAllView==============================
class CouponCodeListView(TemplateView):
    def get(self, request, *args, **kwargs):
        coupon_code = Coupon.objects.all().order_by('-valid_from')
        context = {
            'coupon_code': coupon_code
        }
        return render(request, 'admin/couponcode/couponcode.html', context)


    def post(self, request, *args, **kwargs):
        pass



class CreateNewCouponCodeView(TemplateView):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_staff or request.user.is_admin or request.user.is_superuser:
                form = CouponCodeForm()
                context = {
                    'form': form
                }
                return render(request, 'admin/couponcode/create_coupon_code.html', context)
            else:
                return redirect('store:products')
        else:
            return redirect('store:products')

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated and (request.user.is_staff or request.user.is_admin or request.user.is_superuser):
            form = CouponCodeForm(request.POST, request.FILES)
            if form.is_valid():
                coupon = form.save(commit=False)
                # variation_category.id = slugify(variation_category.id)
                coupon.save()
                return redirect('dashboard:coupon_code')
            else:
                coupon_code = Coupon.objects.all()
                context = {
                    'form': form,
                    'coupon_code': coupon_code
                }
                return render(request, 'admin/coupon/create_coupon_code.html', context)
        else:
            return redirect('store:products')



class UpdateCouponCodeView(TemplateView):
    template_name = 'admin/couponcode/edit_coupon_code.html'

    def get(self, request, pk, *args, **kwargs):
        if request.user.is_authenticated and (request.user.is_staff or request.user.is_admin or request.user.is_superuser):
            try:
                coupon = Coupon.objects.get(pk=pk)
                form = CouponCodeForm(instance=coupon)
                context = {
                    'form': form,
                    'coupon': coupon
                }
                return render(request, self.template_name, context)
            except Coupon.DoesNotExist:
                return redirect('store:products')
        else:
            return redirect('store:products')

    def post(self, request, pk, *args, **kwargs):
        if request.user.is_authenticated and (request.user.is_staff or request.user.is_admin or request.user.is_superuser):
            try:
                coupon_code = Coupon.objects.get(pk=pk)
                form = CouponCodeForm(request.POST, request.FILES, instance=coupon_code)
                if form.is_valid():
                    coupon = form.save(commit=False)
                    coupon.save()
                    return redirect('dashboard:coupon_code')
                else:
                    context = {
                        'form': form,
                        'coupon_code': coupon_code
                    }
                    return render(request, self.template_name, context)
            except Coupon.DoesNotExist:
                return redirect('store:products')
        else:
            return redirect('store:products')

class CouponCodeDeleteView(TemplateView):
    def get(self, request, pk, *args, **kwargs):
        if request.user.is_authenticated and (request.user.is_staff or request.user.is_admin or request.user.is_superuser):
            try:
                coupon_code = Coupon.objects.get(pk=pk)
                coupon_code.delete()
            except Coupon.DoesNotExist:
                pass
            return redirect('dashboard:coupon_code')
        else:
            return redirect('store:products')


# ==========================OrdersAllView==============================

class OrderListView(TemplateView):
    def get(self, request, *args, **kwargs):
        orders = Orders.objects.all().order_by('-order_placed_at')
        context = {
            'orders': orders
        }
        return render(request, 'admin/order/order.html', context)


    def post(self, request, *args, **kwargs):
        pass



class CreateNewOrderView(TemplateView):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_staff or request.user.is_admin or request.user.is_superuser:
                form = OrderForm()
                context = {
                    'form': form
                }
                return render(request, 'admin/order/create_order.html', context)
            else:
                return redirect('store:products')
        else:
            return redirect('store:products')

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated and (request.user.is_staff or request.user.is_admin or request.user.is_superuser):
            form = OrderForm(request.POST, request.FILES)
            if form.is_valid():
                order = form.save(commit=False)
                # variation_category.id = slugify(variation_category.id)
                order.save()
                return redirect('dashboard:order')
            else:
                orders = Orders.objects.all()
                context = {
                    'form': form,
                    'orders': orders
                }
                return render(request, 'admin/order/create_order.html', context)
        else:
            return redirect('store:products')



class UpdateOrderView(TemplateView):
    template_name = 'admin/order/edit_order.html'

    def get(self, request, pk, *args, **kwargs):
        if request.user.is_authenticated and (request.user.is_staff or request.user.is_admin or request.user.is_superuser):
            try:
                order_id = Orders.objects.get(pk=pk)
                form = OrderForm(instance=order_id)
                context = {
                    'form': form,
                    'order_id': order_id
                }
                return render(request, self.template_name, context)
            except Orders.DoesNotExist:
                return redirect('store:products')
        else:
            return redirect('store:products')

    def post(self, request, pk, *args, **kwargs):
        if request.user.is_authenticated and (request.user.is_staff or request.user.is_admin or request.user.is_superuser):
            try:
                order_id = Orders.objects.get(pk=pk)
                form = OrderForm(request.POST, request.FILES, instance=order_id)
                if form.is_valid():
                    order = form.save(commit=False)
                    order.save()
                    return redirect('dashboard:order')
                else:
                    context = {
                        'form': form,
                        'order_id': order_id
                    }
                    return render(request, self.template_name, context)
            except Orders.DoesNotExist:
                return redirect('store:products')
        else:
            return redirect('store:products')

class OrderDeleteView(TemplateView):
    def get(self, request, pk, *args, **kwargs):
        if request.user.is_authenticated and (request.user.is_staff or request.user.is_admin or request.user.is_superuser):
            try:
                order = Orders.objects.get(pk=pk)
                order.delete()
            except Orders.DoesNotExist:
                pass
            return redirect('dashboard:order')
        else:
            return redirect('store:products')




# ==========================OrderItemAllView==============================

class OrderItemListView(TemplateView):
    def get(self, request, *args, **kwargs):
        order_items = OrderItem.objects.all()
        context = {
            'order_items': order_items
        }
        return render(request, 'admin/order/order_item.html', context)


    def post(self, request, *args, **kwargs):
        pass



class CreateNewOrderItemView(TemplateView):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_staff or request.user.is_admin or request.user.is_superuser:
                form = OrderItemForm()
                context = {
                    'form': form
                }
                return render(request, 'admin/order/create_order_item.html', context)
            else:
                return redirect('store:products')
        else:
            return redirect('store:products')

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated and (request.user.is_staff or request.user.is_admin or request.user.is_superuser):
            form = OrderItemForm(request.POST, request.FILES)
            if form.is_valid():
                order_item = form.save(commit=False)
                # variation_category.id = slugify(variation_category.id)
                order_item.save()
                return redirect('dashboard:order_item')
            else:
                order_items = OrderItem.objects.all()
                context = {
                    'form': form,
                    'order_items': order_items
                }
                return render(request, 'admin/order/create_order_item.html', context)
        else:
            return redirect('store:products')



class UpdateOrderItemView(TemplateView):
    template_name = 'admin/order/edit_order_item.html'

    def get(self, request, pk, *args, **kwargs):
        if request.user.is_authenticated and (request.user.is_staff or request.user.is_admin or request.user.is_superuser):
            try:
                order_item_id = OrderItem.objects.get(pk=pk)
                form = OrderItemForm(instance=order_item_id)
                context = {
                    'form': form,
                    'order_item_id': order_item_id
                }
                return render(request, self.template_name, context)
            except OrderItem.DoesNotExist:
                return redirect('store:products')
        else:
            return redirect('store:products')

    def post(self, request, pk, *args, **kwargs):
        if request.user.is_authenticated and (request.user.is_staff or request.user.is_admin or request.user.is_superuser):
            try:
                order_item_id = OrderItem.objects.get(pk=pk)
                form = OrderItemForm(request.POST, request.FILES, instance=order_item_id)
                if form.is_valid():
                    order_item_id = form.save(commit=False)
                    order_item_id.save()
                    return redirect('dashboard:order_item')
                else:
                    context = {
                        'form': form,
                        'order_item_id': order_item_id
                    }
                    return render(request, self.template_name, context)
            except OrderItem.DoesNotExist:
                return redirect('store:products')
        else:
            return redirect('store:products')

class OrderItemDeleteView(TemplateView):
    def get(self, request, pk, *args, **kwargs):
        if request.user.is_authenticated and (request.user.is_staff or request.user.is_admin or request.user.is_superuser):
            try:
                order_item_id = OrderItem.objects.get(pk=pk)
                order_item_id.delete()
            except OrderItem.DoesNotExist:
                pass
            return redirect('dashboard:order_item')
        else:
            return redirect('store:products')






# ==========================ShippingAllView==============================
class ShippingListView(TemplateView):
    def get(self, request, *args, **kwargs):
        shipping = Shipping.objects.all()
        context = {
            'shipping': shipping
        }
        return render(request, 'admin/order/shipping.html', context)


    def post(self, request, *args, **kwargs):
        pass
        

class CreateShippingView(TemplateView):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_staff or request.user.is_admin or request.user.is_superuser:
                form = ShippingForm()
                context = {
                    'form': form
                }
                return render(request, 'admin/order/create_shipping.html', context)
            else:
                return redirect('store:products')
        else:
            return redirect('store:products')

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated and (request.user.is_staff or request.user.is_admin or request.user.is_superuser):
            form = ShippingForm(request.POST, request.FILES)
            if form.is_valid():
                shipping = form.save(commit=False)
                # variation_category.id = slugify(variation_category.id)
                shipping.save()
                return redirect('dashboard:shipping')
            else:
                shipped = Shipping.objects.all()
                context = {
                    'form': form,
                    'shipped': shipped
                }
                return render(request, 'admin/order/create_shipping.html', context)
        else:
            return redirect('store:products')



class UpdateShippingView(TemplateView):
    template_name = 'admin/order/edit_shipping.html'

    def get(self, request, pk, *args, **kwargs):
        if request.user.is_authenticated and (request.user.is_staff or request.user.is_admin or request.user.is_superuser):
            try:
                shipped = Shipping.objects.get(pk=pk)
                form = ShippingForm(instance=shipped)
                context = {
                    'form': form,
                    'shipped': shipped
                }
                return render(request, self.template_name, context)
            except Shipping.DoesNotExist:
                return redirect('store:products')
        else:
            return redirect('store:products')

    def post(self, request, pk, *args, **kwargs):
        if request.user.is_authenticated and (request.user.is_staff or request.user.is_admin or request.user.is_superuser):
            try:
                shipped = Shipping.objects.get(pk=pk)
                form = ShippingForm(request.POST, request.FILES, instance=shipped)
                if form.is_valid():
                    shipped = form.save(commit=False)
                    shipped.save()
                    return redirect('dashboard:shipping')
                else:
                    context = {
                        'form': form,
                        'shipped': shipped
                    }
                    return render(request, self.template_name, context)
            except Shipping.DoesNotExist:
                return redirect('store:products')
        else:
            return redirect('store:products')

class ShippingDeleteView(TemplateView):
    def get(self, request, pk, *args, **kwargs):
        if request.user.is_authenticated and (request.user.is_staff or request.user.is_admin or request.user.is_superuser):
            try:
                shipped = Shipping.objects.get(pk=pk)
                shipped.delete()
            except Shipping.DoesNotExist:
                pass
            return redirect('dashboard:shipping')
        else:
            return redirect('store:products')



# ==========================PaymentAllView==============================

class PaymentListView(TemplateView):
    def get(self, request, *args, **kwargs):
        payment = Payment.objects.all().order_by('-created_at')
        context = {
            'payment': payment
        }
        return render(request, 'admin/payment/payment.html', context)


    def post(self, request, *args, **kwargs):
        pass
        

class CreatePaymentView(TemplateView):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_staff or request.user.is_admin or request.user.is_superuser:
                form = PaymentForm()
                context = {
                    'form': form
                }
                return render(request, 'admin/payment/create_payment.html', context)
            else:
                return redirect('store:products')
        else:
            return redirect('store:products')

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated and (request.user.is_staff or request.user.is_admin or request.user.is_superuser):
            form = PaymentForm(request.POST, request.FILES)
            if form.is_valid():
                pay = form.save(commit=False)
                # variation_category.id = slugify(variation_category.id)
                pay.save()
                return redirect('dashboard:payment')
            else:
                payment = Payment.objects.all()
                context = {
                    'form': form,
                    'payment': payment
                }
                return render(request, 'admin/payment/create_payment.html', context)
        else:
            return redirect('store:products')



class UpdatePaymentView(TemplateView):
    template_name = 'admin/payment/edit_payment.html'

    def get(self, request, pk, *args, **kwargs):
        if request.user.is_authenticated and (request.user.is_staff or request.user.is_admin or request.user.is_superuser):
            try:
                payment = Payment.objects.get(pk=pk)
                form = PaymentForm(instance=payment)
                context = {
                    'form': form,
                    'payment': payment
                }
                return render(request, self.template_name, context)
            except Payment.DoesNotExist:
                return redirect('store:products')
        else:
            return redirect('store:products')

    def post(self, request, pk, *args, **kwargs):
        if request.user.is_authenticated and (request.user.is_staff or request.user.is_admin or request.user.is_superuser):
            try:
                payment = Payment.objects.get(pk=pk)
                form = PaymentForm(request.POST, request.FILES, instance=payment)
                if form.is_valid():
                    pay = form.save(commit=False)
                    pay.save()
                    return redirect('dashboard:payment')
                else:
                    context = {
                        'form': form,
                        'payment': payment
                    }
                    return render(request, self.template_name, context)
            except Payment.DoesNotExist:
                return redirect('store:products')
        else:
            return redirect('store:products')

class PaymentDeleteView(TemplateView):
    def get(self, request, pk, *args, **kwargs):
        if request.user.is_authenticated and (request.user.is_staff or request.user.is_admin or request.user.is_superuser):
            try:
                payment = Payment.objects.get(pk=pk)
                payment.delete()
            except Payment.DoesNotExist:
                pass
            return redirect('dashboard:payment')
        else:
            return redirect('store:products')


# ==========================ReviewAllView==============================
class ReviewListView(TemplateView):
    def get(self, request, *args, **kwargs):
        reviews = Review.objects.all().order_by('-created_at')
        context = {
            'reviews': reviews
        }
        return render(request, 'admin/product_utils/review.html', context)


    def post(self, request, *args, **kwargs):
        pass
        

class CreateReviewView(TemplateView):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_staff or request.user.is_admin or request.user.is_superuser:
                form = ReviewForm()
                context = {
                    'form': form
                }
                return render(request, 'admin/product_utils/create_review.html', context)
            else:
                return redirect('store:products')
        else:
            return redirect('store:products')

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated and (request.user.is_staff or request.user.is_admin or request.user.is_superuser):
            form = ReviewForm(request.POST, request.FILES)
            if form.is_valid():
                review = form.save(commit=False)
                # variation_category.id = slugify(variation_category.id)
                review.save()
                return redirect('dashboard:payment')
            else:
                reviews = Payment.objects.all()
                context = {
                    'form': form,
                    'reviews': reviews
                }
                return render(request, 'admin/product_utils/create_review.html', context)
        else:
            return redirect('store:products')



class UpdateReviewView(TemplateView):
    template_name = 'admin/product_utils/edit_review.html'

    def get(self, request, pk, *args, **kwargs):
        if request.user.is_authenticated and (request.user.is_staff or request.user.is_admin or request.user.is_superuser):
            try:
                reviews = Review.objects.get(pk=pk)
                form = PaymentForm(instance=reviews)
                context = {
                    'form': form,
                    'reviews': reviews
                }
                return render(request, self.template_name, context)
            except Review.DoesNotExist:
                return redirect('store:products')
        else:
            return redirect('store:products')

    def post(self, request, pk, *args, **kwargs):
        if request.user.is_authenticated and (request.user.is_staff or request.user.is_admin or request.user.is_superuser):
            try:
                reviews = Review.objects.get(pk=pk)
                form = ReviewForm(request.POST, request.FILES, instance=reviews)
                if form.is_valid():
                    review = form.save(commit=False)
                    review.save()
                    return redirect('dashboard:review')
                else:
                    context = {
                        'form': form,
                        'reviews': reviews
                    }
                    return render(request, self.template_name, context)
            except Review.DoesNotExist:
                return redirect('store:products')
        else:
            return redirect('store:products')

class ReviewDeleteView(TemplateView):
    def get(self, request, pk, *args, **kwargs):
        if request.user.is_authenticated and (request.user.is_staff or request.user.is_admin or request.user.is_superuser):
            try:
                review = Review.objects.get(pk=pk)
                review.delete()
            except Review.DoesNotExist:
                pass
            return redirect('dashboard:review')
        else:
            return redirect('store:products')






# ==========================CompareAllView==============================

class CompareListView(TemplateView):
    def get(self, request, *args, **kwargs):
        compares = Compare.objects.all()
        context = {
            'compares': compares
        }
        return render(request, 'admin/product_utils/compare.html', context)


    def post(self, request, *args, **kwargs):
        pass
        

class CreateCompareView(TemplateView):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_staff or request.user.is_admin or request.user.is_superuser:
                form = CompareForm()
                context = {
                    'form': form
                }
                return render(request, 'admin/product_utils/create_compare.html', context)
            else:
                return redirect('store:products')
        else:
            return redirect('store:products')

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated and (request.user.is_staff or request.user.is_admin or request.user.is_superuser):
            form = CompareForm(request.POST, request.FILES)
            if form.is_valid():
                compare = form.save(commit=False)
                # variation_category.id = slugify(variation_category.id)
                compare.save()
                return redirect('dashboard:compare')
            else:
                compares = Compare.objects.all()
                context = {
                    'form': form,
                    'compares': compares
                }
                return render(request, 'admin/product_utils/create_compare.html', context)
        else:
            return redirect('store:products')



class UpdateCompareView(TemplateView):
    template_name = 'admin/product_utils/edit_compare.html'

    def get(self, request, pk, *args, **kwargs):
        if request.user.is_authenticated and (request.user.is_staff or request.user.is_admin or request.user.is_superuser):
            try:
                compare = Compare.objects.get(pk=pk)
                form = CompareForm(instance=compare)
                context = {
                    'form': form,
                    'compare': compare
                }
                return render(request, self.template_name, context)
            except Compare.DoesNotExist:
                return redirect('store:products')
        else:
            return redirect('store:products')

    def post(self, request, pk, *args, **kwargs):
        if request.user.is_authenticated and (request.user.is_staff or request.user.is_admin or request.user.is_superuser):
            try:
                compares = Compare.objects.get(pk=pk)
                form = CompareForm(request.POST, request.FILES, instance=compare)
                if form.is_valid():
                    compare = form.save(commit=False)
                    compare.save()
                    return redirect('dashboard:compare')
                else:
                    context = {
                        'form': form,
                        'compares': compares
                    }
                    return render(request, self.template_name, context)
            except Compare.DoesNotExist:
                return redirect('store:products')
        else:
            return redirect('store:products')

class CompareDeleteView(TemplateView):
    def get(self, request, pk, *args, **kwargs):
        if request.user.is_authenticated and (request.user.is_staff or request.user.is_admin or request.user.is_superuser):
            try:
                compare = Compare.objects.get(pk=pk)
                compare.delete()
            except Compare.DoesNotExist:
                pass
            return redirect('dashboard:compare')
        else:
            return redirect('store:products')





# ==========================WishlistAllView==============================


class WishlistListView(TemplateView):
    def get(self, request, *args, **kwargs):
        wishlist = Wishlist.objects.all()
        context = {
            'wishlist': wishlist
        }
        return render(request, 'admin/product_utils/wishlist.html', context)


    def post(self, request, *args, **kwargs):
        pass
        

class CreateWishlistView(TemplateView):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_staff or request.user.is_admin or request.user.is_superuser:
                form = WishlistForm()
                context = {
                    'form': form
                }
                return render(request, 'admin/product_utils/create_wishlist.html', context)
            else:
                return redirect('store:products')
        else:
            return redirect('store:products')

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated and (request.user.is_staff or request.user.is_admin or request.user.is_superuser):
            form = WishlistForm(request.POST, request.FILES)
            if form.is_valid():
                wishlist = form.save(commit=False)
                # variation_category.id = slugify(variation_category.id)
                wishlist.save()
                return redirect('dashboard:wishlist')
            else:
                wish = Wishlist.objects.all()
                context = {
                    'form': form,
                    'wish': wish
                }
                return render(request, 'admin/product_utils/create_wishlist.html', context)
        else:
            return redirect('store:products')



class UpdateWishlistView(TemplateView):
    template_name = 'admin/product_utils/edit_wishlist.html'

    def get(self, request, pk, *args, **kwargs):
        if request.user.is_authenticated and (request.user.is_staff or request.user.is_admin or request.user.is_superuser):
            try:
                wishlist = Wishlist.objects.get(pk=pk)
                form = WishlistForm(instance=wishlist)
                context = {
                    'form': form,
                    'wishlist': wishlist
                }
                return render(request, self.template_name, context)
            except Wishlist.DoesNotExist:
                return redirect('store:products')
        else:
            return redirect('store:products')

    def post(self, request, pk, *args, **kwargs):
        if request.user.is_authenticated and (request.user.is_staff or request.user.is_admin or request.user.is_superuser):
            try:
                wishlist = Wishlist.objects.get(pk=pk)
                form = WishlistForm(request.POST, request.FILES, instance=wishlist)
                if form.is_valid():
                    wish = form.save(commit=False)
                    wish.save()
                    return redirect('dashboard:wishlist')
                else:
                    context = {
                        'form': form,
                        'wishlist': wishlist
                    }
                    return render(request, self.template_name, context)
            except Wishlist.DoesNotExist:
                return redirect('store:products')
        else:
            return redirect('store:products')

class WishlistDeleteView(TemplateView):
    def get(self, request, pk, *args, **kwargs):
        if request.user.is_authenticated and (request.user.is_staff or request.user.is_admin or request.user.is_superuser):
            try:
                wishlist = Wishlist.objects.get(pk=pk)
                wishlist.delete()
            except Wishlist.DoesNotExist:
                pass
            return redirect('dashboard:wishlist')
        else:
            return redirect('store:products')



# ==========================UserAccountsAllView==============================

class UserListView(TemplateView):
    def get(self, request, *args, **kwargs):
        users = UserAccount.objects.all()
        context = {
            'users': users
        }
        return render(request, 'admin/user/user.html', context)


    def post(self, request, *args, **kwargs):
        pass
        



