# Generated by Django 2.2.11 on 2020-03-22 19:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('euphonime', '0006_usermessage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usermessage',
            name='is_replied',
        ),
        migrations.RemoveField(
            model_name='usermessage',
            name='reply',
        ),
    ]
