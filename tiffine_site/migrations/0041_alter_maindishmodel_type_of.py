# Generated by Django 4.0.1 on 2023-02-13 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tiffine_site', '0040_alter_maindishmodel_type_of'),
    ]

    operations = [
        migrations.AlterField(
            model_name='maindishmodel',
            name='type_of',
            field=models.CharField(blank=True, choices=[('VRG', 'VEG'), ('NON-VEG', 'NON-VEG')], max_length=10),
        ),
    ]
