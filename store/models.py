import uuid
from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.template.defaultfilters import default, slugify


# Create your models here.


# ========================Category===============================
class Category(models.Model):
    category_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category_title = models.CharField(max_length=200, unique=True, blank=True)
    slug = models.SlugField(max_length=255, unique=True, default='')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='sub_categories')

    category_desc = models.TextField(max_length=255, blank=True)
    category_image = models.ImageField(upload_to='photos/categories/', blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at', ]
        verbose_name_plural = 'Category'

    def __str__(self):
        return self.category_title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.category_title)
        return super().save(*args, **kwargs)


# ========================Products===============================
class Products(models.Model):
    product_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product_title = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    short_description = models.CharField(max_length=255, default='', verbose_name='Short Descriptions')
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category')
    image = models.ImageField(upload_to='photos/product_image/')
    stock = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=100, decimal_places=2)
    old_price = models.DecimalField(max_digits=100, decimal_places=2, default=0.00, blank=True, null=True)

    is_available = models.BooleanField(default=True)
    top_deal=models.BooleanField(default=False)
    flash_sales = models.BooleanField(default=False)
    is_out_of_stock = models.BooleanField(default=False)


    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'products'
        verbose_name_plural = 'products'
        ordering = ['-created_at']
        

    def __str__(self):
        return self.product_title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.product_title)
        return super().save(*args, **kwargs)
    

    def check_stock(self):
        if self.stock <= 0:
            self.is_out_of_stock = True
        else:
            self.is_out_of_stock = False
        self.save()
    

# ========================ProductImages===============================
class ProductImages(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    product_images = models.FileField(upload_to='photos/product_gallery/')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Product Images'

    def __str__(self):
        return str(self.product.product_title)
    


# ========================ProductVariationCategory===============================
class ProductVariationCategory(models.Model):
    variation_category_title = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at', ]
        verbose_name_plural = 'Variation Categories'

    def __str__(self):
        return self.variation_category_title

# ========================ProductVariation===============================
class ProductVariation(models.Model):
    variation_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    variation_value = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    variation_category = models.ForeignKey(ProductVariationCategory, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='products')
    # slug = models.SlugField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at', ]
        verbose_name_plural = 'Product Variations'

    def __str__(self):
        return self.variation_value
    


