# Generated by Django 5.0.6 on 2024-05-22 09:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_alter_orderitems_product_variation'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='shipping_option',
        ),
        migrations.RemoveField(
            model_name='order',
            name='total_price',
        ),
    ]