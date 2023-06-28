# Generated by Django 4.1.7 on 2023-06-05 21:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dashboard', '0004_product_created_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.CharField(max_length=200, null=True)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('confirmed', 'confirmed'), ('Delivered', 'Delivered')], max_length=11, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('ordered_by', models.ForeignKey(max_length=11, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('product_name', models.ForeignKey(max_length=11, null=True, on_delete=django.db.models.deletion.SET_NULL, to='dashboard.product')),
            ],
        ),
    ]