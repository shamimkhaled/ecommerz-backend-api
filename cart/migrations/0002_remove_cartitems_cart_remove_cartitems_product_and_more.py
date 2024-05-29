# Generated by Django 5.0.6 on 2024-05-19 09:29

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0001_initial'),
        ('store', '0006_productvariation_price'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitems',
            name='cart',
        ),
        migrations.RemoveField(
            model_name='cartitems',
            name='product',
        ),
        migrations.RemoveField(
            model_name='cartitems',
            name='product_variation',
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='store.products')),
                ('product_variation', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='store.productvariation')),
            ],
        ),
        migrations.CreateModel(
            name='Carts',
            fields=[
                ('cart_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('products', models.ManyToManyField(through='cart.CartItem', to='store.products')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cart', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='cartitem',
            name='cart',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cartitems', to='cart.carts'),
        ),
        migrations.DeleteModel(
            name='Cart',
        ),
        migrations.DeleteModel(
            name='CartItems',
        ),
    ]
