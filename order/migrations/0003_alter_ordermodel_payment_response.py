# Generated by Django 4.0.1 on 2023-02-12 05:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_ordermodel_payment_signature_userdetail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordermodel',
            name='payment_response',
            field=models.JSONField(),
        ),
    ]