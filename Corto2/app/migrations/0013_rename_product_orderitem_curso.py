# Generated by Django 5.1.1 on 2024-10-02 05:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_shippingaddress'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderitem',
            old_name='product',
            new_name='curso',
        ),
    ]