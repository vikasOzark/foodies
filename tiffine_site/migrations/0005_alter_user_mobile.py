# Generated by Django 3.2.6 on 2022-03-04 06:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tiffine_site', '0004_addressmodel_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='mobile',
            field=models.IntegerField(blank=True),
        ),
    ]