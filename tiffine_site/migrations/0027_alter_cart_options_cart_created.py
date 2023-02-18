# Generated by Django 4.0.1 on 2023-01-29 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tiffine_site', '0026_cart_is_complete'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cart',
            options={'get_latest_by': '-created'},
        ),
        migrations.AddField(
            model_name='cart',
            name='created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
