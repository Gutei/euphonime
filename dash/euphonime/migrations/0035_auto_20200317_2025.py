# Generated by Django 2.2.11 on 2020-03-17 13:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('euphonime', '0034_auto_20200317_2018'),
    ]

    operations = [
        migrations.AlterField(
            model_name='animeseason',
            name='anime',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='euphonime.Anime'),
        ),
        migrations.AlterField(
            model_name='animeseason',
            name='season',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='euphonime.Season'),
        ),
    ]