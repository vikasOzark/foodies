# Generated by Django 4.0.1 on 2023-02-03 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tiffine_site', '0039_commentandrating_is_show'),
    ]

    operations = [
        migrations.AlterField(
            model_name='maindishmodel',
            name='type_of',
            field=models.CharField(blank=True, choices=[('veg', '🥝'), ('non_veg', '🍗')], max_length=10),
        ),
    ]
