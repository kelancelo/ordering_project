# Generated by Django 4.1.4 on 2022-12-16 08:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ordering_app', '0002_kiosk_product_remove_cart_product_add_ons_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addon',
            name='image_url',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='product',
            name='image_url',
            field=models.CharField(max_length=200),
        ),
    ]