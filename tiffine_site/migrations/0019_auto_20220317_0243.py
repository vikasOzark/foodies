# Generated by Django 3.2.6 on 2022-03-17 02:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tiffine_site', '0018_auto_20220316_2054'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderdetails',
            name='qyt_3',
            field=models.PositiveIntegerField(blank=True, default=1, null=True),
        ),
        migrations.AddField(
            model_name='orderdetails',
            name='qyt_4',
            field=models.PositiveBigIntegerField(blank=True, default=1, null=True),
        ),
        migrations.AddField(
            model_name='orderdetails',
            name='qyt_5',
            field=models.PositiveBigIntegerField(blank=True, default=1, null=True),
        ),
    ]