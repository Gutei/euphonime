# Generated by Django 2.2.11 on 2020-04-02 09:29

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('euphonime', '0008_userpost'),
    ]

    operations = [
        migrations.CreateModel(
            name='MetaGeneral',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('meta_name', models.CharField(default='-', max_length=128)),
                ('value', models.TextField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'meta_generals',
            },
        ),
    ]
