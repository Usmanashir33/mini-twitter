# Generated by Django 4.2.4 on 2023-09-13 23:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_rename_followers_user_followings'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='title',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]