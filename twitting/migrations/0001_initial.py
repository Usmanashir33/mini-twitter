# Generated by Django 4.2.4 on 2023-09-23 13:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(help_text='Write Your Post Here!', max_length=100)),
                ('post_file', models.FileField(blank=True, null=True, upload_to='post_media')),
                ('post_date', models.DateTimeField(auto_now_add=True)),
                ('views', models.IntegerField(blank=True)),
                ('likes', models.ManyToManyField(blank=True, related_name='post_likes', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Tweet',
                'ordering': ['-post_date'],
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(help_text='Comment Here!', max_length=100)),
                ('comment_date', models.DateTimeField(auto_now_add=True)),
                ('comment_file', models.FileField(blank=True, null=True, upload_to='comments_media')),
                ('views', models.IntegerField(blank=True)),
                ('likes', models.ManyToManyField(blank=True, related_name='comment_likes', to=settings.AUTH_USER_MODEL)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='twitting.comment')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='twitting.post')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-comment_date'],
            },
        ),
    ]