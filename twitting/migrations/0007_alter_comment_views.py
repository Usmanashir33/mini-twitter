# Generated by Django 4.2.4 on 2023-09-23 21:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twitting', '0006_alter_post_views'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='views',
            field=models.PositiveBigIntegerField(blank=True, default=0),
        ),
    ]
