# Generated by Django 4.2.4 on 2023-09-10 11:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_alter_user_followers'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='Followers',
            new_name='Followings',
        ),
    ]