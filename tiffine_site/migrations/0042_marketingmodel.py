# Generated by Django 4.0.1 on 2023-02-14 07:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tiffine_site', '0041_alter_maindishmodel_type_of'),
    ]

    operations = [
        migrations.CreateModel(
            name='MarketingModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='marketing/')),
            ],
        ),
    ]
