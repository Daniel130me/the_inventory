# Generated by Django 4.1.7 on 2023-06-06 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0006_rename_product_name_order_product_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Canceled', 'Canceled'), ('confirmed', 'confirmed'), ('Delivered', 'Delivered')], max_length=11, null=True),
        ),
    ]
