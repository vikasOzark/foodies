# Generated by Django 4.0.1 on 2023-02-18 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0004_remove_bannersmodel_itmes_bannersmodel_itmes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bannersmodel',
            name='text',
            field=models.TextField(blank=True, null=True),
        ),
    ]
