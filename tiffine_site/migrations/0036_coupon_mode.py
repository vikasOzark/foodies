# Generated by Django 4.0.1 on 2023-01-31 03:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tiffine_site', '0035_alter_cart_coupond_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='coupon',
            name='mode',
            field=models.CharField(choices=[('COD', 'COD'), ('ONLINE', 'ONLINE')], default='ONLINE', max_length=20),
        ),
    ]