# Generated by Django 4.0.1 on 2023-02-04 03:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tiffine_site', '0040_alter_maindishmodel_type_of'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(max_length=100, unique=True)),
                ('payment_status', models.CharField(choices=[('PENDING', 'PENDING'), ('CONFIRM', 'CONFIRM'), ('CANCEL', 'CANCEL'), ('FAILD', 'FAILD')], default='PENDING', max_length=30)),
                ('payment_id', models.CharField(max_length=255, null=True)),
                ('payment_response', models.TextField()),
                ('payment_mathod', models.CharField(choices=[('COD', 'COD'), ('ONLINE', 'ONLINE')], max_length=30, null=True)),
                ('payment_partner', models.CharField(choices=[('RAZORPAY', 'RAZORPAY')], max_length=30, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='tiffine_site.addressmodel')),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tiffine_site.cart')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
