# Generated by Django 4.0.1 on 2023-01-30 19:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tiffine_site', '0033_deliverycharges'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='coupon_used',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='cart',
            name='coupond_amount',
            field=models.CharField(max_length=20, null=True),
        ),
    ]