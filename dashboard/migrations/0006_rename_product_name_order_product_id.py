# Generated by Django 4.1.7 on 2023-06-05 21:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0005_order'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='product_name',
            new_name='product_id',
        ),
    ]
