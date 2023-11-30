# Generated by Django 4.2.4 on 2023-10-11 14:02

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('twitting', '0007_alter_comment_views'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='repost',
            field=models.ManyToManyField(blank=True, related_name='reposts', to=settings.AUTH_USER_MODEL),
        ),
    ]