# Generated by Django 4.1.7 on 2023-06-07 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0007_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Canceled', 'Canceled'), ('Confirmed', 'Confirmed'), ('Delivered', 'Delivered')], max_length=11, null=True),
        ),
    ]
