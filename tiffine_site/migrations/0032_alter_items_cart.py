# Generated by Django 4.0.1 on 2023-01-30 17:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tiffine_site', '0031_alter_items_quantity_alter_items_unit_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='items',
            name='cart',
            field=models.CharField(max_length=20),
        ),
    ]