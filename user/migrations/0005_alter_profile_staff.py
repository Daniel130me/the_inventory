# Generated by Django 4.1.7 on 2023-06-11 16:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_alter_profile_staff'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='staff',
            field=models.OneToOneField(default=16, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
