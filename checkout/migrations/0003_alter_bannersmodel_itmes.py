# Generated by Django 4.0.1 on 2023-02-16 04:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tiffine_site', '0043_alter_addressmodel_city_alter_addressmodel_landmark_and_more'),
        ('checkout', '0002_bannersmodel_image_bannersmodel_validity_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bannersmodel',
            name='itmes',
            field=models.ManyToManyField(to='tiffine_site.MainDishModel'),
        ),
    ]
