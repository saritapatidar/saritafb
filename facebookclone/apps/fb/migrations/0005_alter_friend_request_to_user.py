# Generated by Django 4.2.20 on 2025-04-11 06:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fb', '0004_friend_request'),
    ]

    operations = [
        migrations.AlterField(
            model_name='friend_request',
            name='to_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_user', to=settings.AUTH_USER_MODEL),
        ),
    ]
