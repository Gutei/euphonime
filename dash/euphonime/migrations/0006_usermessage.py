# Generated by Django 2.2.11 on 2020-03-22 19:28

import ckeditor_uploader.fields
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('euphonime', '0005_profileuser_symbol'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserMessage',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('message', models.TextField(blank=True, null=True)),
                ('reply', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True)),
                ('is_replied', models.BooleanField(default=False, verbose_name='Dibalas')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='euphonime.ProfileUser')),
            ],
            options={
                'verbose_name': 'Pesan Untuk Developer',
                'db_table': 'user_messages',
            },
        ),
    ]