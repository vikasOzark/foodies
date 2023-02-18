# Generated by Django 4.0.1 on 2023-02-04 03:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tiffine_site', '0040_alter_maindishmodel_type_of'),
    ]

    operations = [
        migrations.CreateModel(
            name='BannersModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('banner_type', models.ImageField(choices=[('HOME_CAROSEL', 'HOME_CAROSEL'), ('MENU_CAROCEL', 'MENU_CAROCEL'), ('CART_IMG', 'CART_IMG'), ('ADDRESS_IMG', 'ADDRESS_IMG'), ('PAYMENT_IMG', 'PAYMENT_IMG')], upload_to='products')),
                ('text', models.TextField(null=True)),
                ('crested_at', models.DateTimeField(auto_now_add=True)),
                ('itmes', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tiffine_site.maindishmodel')),
            ],
        ),
    ]