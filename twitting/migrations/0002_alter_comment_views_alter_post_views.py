# Generated by Django 4.2.4 on 2023-09-23 21:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twitting', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='views',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='views',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
