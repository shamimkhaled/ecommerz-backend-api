# Generated by Django 5.0.6 on 2024-05-26 05:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0006_remove_orderitems_order_remove_orderitems_product_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='total_amount',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=100),
        ),
    ]
