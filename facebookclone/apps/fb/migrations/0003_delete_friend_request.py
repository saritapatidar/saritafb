# Generated by Django 4.2.20 on 2025-04-11 06:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fb', '0002_rename_to_friend_request_to_user_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Friend_request',
        ),
    ]
