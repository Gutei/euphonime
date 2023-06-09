# Generated by Django 2.2.11 on 2020-03-19 23:13

import ckeditor_uploader.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Anime',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('image', models.ImageField(blank=True, max_length=1500, null=True, upload_to='anime/image')),
                ('image_url', models.CharField(blank=True, max_length=1500, null=True)),
                ('title', models.CharField(default='-', max_length=128)),
                ('native_title', models.CharField(blank=True, max_length=128, null=True)),
                ('english_title', models.CharField(blank=True, max_length=128, null=True)),
                ('type', models.PositiveIntegerField(blank=True, choices=[(1, 'TV'), (2, 'OVA'), (3, 'ONA'), (4, 'OAD'), (5, 'Movie')], null=True)),
                ('description', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True)),
                ('airing_date', models.DateTimeField(blank=True, null=True)),
                ('rating', models.CharField(blank=True, max_length=128, null=True)),
                ('mal_id', models.CharField(blank=True, max_length=128, null=True)),
                ('website', models.TextField(blank=True, null=True)),
                ('total_episode', models.PositiveIntegerField(default=0)),
                ('duration', models.PositiveIntegerField(default=0)),
                ('is_publish', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'anime',
            },
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='anime/image')),
                ('title', models.CharField(default='-', max_length=128)),
                ('content', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True)),
                ('is_publish', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'articles',
            },
        ),
        migrations.CreateModel(
            name='Character',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('image', models.ImageField(blank=True, max_length=1500, null=True, upload_to='character/image')),
                ('image_url', models.CharField(blank=True, max_length=1500, null=True)),
                ('name', models.CharField(default='-', max_length=128)),
                ('native_name', models.CharField(blank=True, max_length=128, null=True)),
                ('description', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True)),
                ('role', models.PositiveIntegerField(blank=True, choices=[(1, 'Main'), (2, 'Support')], null=True)),
                ('mal_id', models.CharField(blank=True, max_length=128, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'characters',
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('title', models.CharField(default='-', max_length=128)),
                ('icon', models.ImageField(blank=True, null=True, upload_to='genre/icon')),
            ],
            options={
                'db_table': 'genres',
            },
        ),
        migrations.CreateModel(
            name='MalAnime',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('mal_id', models.CharField(blank=True, max_length=128, null=True)),
                ('log', models.CharField(blank=True, max_length=128, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Sync from MAL',
                'db_table': 'mal_anime',
            },
        ),
        migrations.CreateModel(
            name='OstAuthor',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(default='-', max_length=128)),
                ('description', models.TextField(blank=True, null=True)),
                ('icon', models.ImageField(blank=True, null=True, upload_to='ost/author/icon')),
            ],
            options={
                'db_table': 'ost_authors',
            },
        ),
        migrations.CreateModel(
            name='Producer',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(default='-', max_length=128)),
                ('description', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'producers',
            },
        ),
        migrations.CreateModel(
            name='ProfileUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo_profile', models.ImageField(blank=True, null=True, upload_to='user/profile')),
                ('biodata', models.TextField(blank=True, null=True)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'user_profiles',
            },
        ),
        migrations.CreateModel(
            name='Season',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(blank=True, max_length=128, null=True)),
                ('is_season', models.BooleanField(default=False, verbose_name='This season')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'seasons',
            },
        ),
        migrations.CreateModel(
            name='Studio',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(default='-', max_length=128)),
                ('description', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'studios',
            },
        ),
        migrations.CreateModel(
            name='VoiceAct',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('image', models.ImageField(blank=True, max_length=1500, null=True, upload_to='seiyuu/image')),
                ('image_url', models.CharField(blank=True, max_length=1500, null=True)),
                ('name', models.CharField(default='-', max_length=128)),
                ('given_name', models.CharField(blank=True, max_length=128, null=True)),
                ('family_name', models.CharField(blank=True, max_length=128, null=True)),
                ('birth_date', models.DateTimeField(blank=True, null=True)),
                ('description', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True)),
                ('mal_id', models.CharField(blank=True, max_length=128, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Voice Actress/Actor',
                'db_table': 'voice_acts',
            },
        ),
        migrations.CreateModel(
            name='UserWatching',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('status', models.PositiveIntegerField(blank=True, choices=[(1, 'Sedang ditonton'), (2, 'Selesai ditonton'), (3, 'Menunda'), (4, 'Tidak melanjutkan')], null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('anime', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='euphonime.Anime')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='euphonime.ProfileUser')),
            ],
            options={
                'db_table': 'user_watching',
            },
        ),
        migrations.CreateModel(
            name='UserPolls',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('poll', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('anime', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='euphonime.Anime')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='euphonime.ProfileUser')),
            ],
            options={
                'verbose_name': 'Polling',
                'db_table': 'user_polls',
            },
        ),
        migrations.CreateModel(
            name='UserAnimeScore',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('score', models.IntegerField(default=0)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('anime', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='euphonime.Anime')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='euphonime.ProfileUser')),
            ],
            options={
                'db_table': 'user_anime_scores',
            },
        ),
        migrations.CreateModel(
            name='SampleVoiceAct',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('title', models.CharField(blank=True, max_length=128, null=True)),
                ('audio', models.FileField(blank=True, null=True, upload_to='seiyuu/audio')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('seiyuu', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='euphonime.VoiceAct')),
            ],
            options={
                'db_table': 'voice_act_samples',
            },
        ),
        migrations.CreateModel(
            name='Quote',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('quote', models.TextField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('character', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='euphonime.Character')),
            ],
            options={
                'db_table': 'quotes',
            },
        ),
        migrations.CreateModel(
            name='Ost',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('title', models.CharField(default='-', max_length=128)),
                ('type', models.PositiveIntegerField(blank=True, choices=[(1, 'Opening Song'), (2, 'Ending Song'), (3, 'Insert Song')], null=True)),
                ('lyric', models.TextField(blank=True, null=True)),
                ('url', models.TextField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('anime', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='euphonime.Anime')),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='euphonime.OstAuthor')),
            ],
            options={
                'verbose_name': 'Original Soundtrack',
                'db_table': 'ost',
            },
        ),
        migrations.AddField(
            model_name='character',
            name='voice_act',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='euphonime.VoiceAct'),
        ),
        migrations.CreateModel(
            name='AnimeStudio',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('anime', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='euphonime.Anime')),
                ('studio', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='euphonime.Studio')),
            ],
            options={
                'db_table': 'anime_studios',
            },
        ),
        migrations.CreateModel(
            name='AnimeSeason',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('anime', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='euphonime.Anime')),
                ('season', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='euphonime.Season')),
            ],
            options={
                'db_table': 'anime_seasons',
            },
        ),
        migrations.CreateModel(
            name='AnimeProducer',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('anime', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='euphonime.Anime')),
                ('producer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='euphonime.Producer')),
            ],
            options={
                'db_table': 'anime_producers',
            },
        ),
        migrations.CreateModel(
            name='AnimeGenre',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('anime', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='euphonime.Anime')),
                ('genre', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='euphonime.Genre')),
            ],
            options={
                'db_table': 'anime_genre',
            },
        ),
        migrations.CreateModel(
            name='AnimeCharacter',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('anime', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='euphonime.Anime')),
                ('character', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='euphonime.Character')),
            ],
            options={
                'db_table': 'anime_characters',
            },
        ),
    ]
