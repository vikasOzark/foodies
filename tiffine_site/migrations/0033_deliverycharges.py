# Generated by Django 4.0.1 on 2023-01-30 19:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tiffine_site', '0032_alter_items_cart'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeliveryCharges',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveIntegerField(default=0)),
                ('is_active', models.BooleanField(default=False)),
            ],
        ),
    ]
