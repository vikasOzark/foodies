# Generated by Django 4.0.1 on 2023-02-28 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tiffine_site', '0045_peoplefavorite'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='peoplefavorite',
            name='food',
        ),
        migrations.AddField(
            model_name='peoplefavorite',
            name='food',
            field=models.ManyToManyField(to='tiffine_site.MainDishModel'),
        ),
    ]