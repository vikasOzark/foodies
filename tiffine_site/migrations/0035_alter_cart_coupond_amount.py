# Generated by Django 4.0.1 on 2023-01-30 19:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tiffine_site', '0034_cart_coupon_used_cart_coupond_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='coupond_amount',
            field=models.CharField(default=0, max_length=20, null=True),
        ),
    ]
