# Generated by Django 2.2.11 on 2020-04-03 07:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('euphonime', '0012_auto_20200402_2011'),
    ]

    operations = [
        migrations.AddField(
            model_name='anime',
            name='slug',
            field=models.SlugField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='article',
            name='slug',
            field=models.SlugField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='character',
            name='slug',
            field=models.SlugField(blank=True, null=True),
        ),
    ]
