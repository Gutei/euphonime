import os
import re
import requests
import uuid
from django.db import models
from django.core.files import File
from .character import Character
from .voice_act import VoiceAct

import logging

from ckeditor.fields import RichTextField
from euphonime.tasks import sync_anime

logger = logging.getLogger(__name__)

class Anime(models.Model):

    TV = 1
    OVA = 2
    ONA = 3
    OAD = 4
    MOVIE = 5

    TYPE = (
        (TV, 'TV'),
        (OVA, 'OVA'),
        (ONA, 'ONA'),
        (OAD, 'OAD'),
        (MOVIE, 'Movie')
    )

    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    image = models.ImageField(upload_to='anime/image', null=True, blank=True, max_length=1500)
    image_url = models.CharField(null=True, blank=True, max_length=1500)
    title = models.CharField(max_length=128, default="-")
    native_title = models.CharField(max_length=128, null=True, blank=True)
    english_title = models.CharField(max_length=128, null=True, blank=True)
    type = models.PositiveIntegerField(choices=TYPE, null=True, blank=True )
    description = RichTextField(blank=True, null=True)
    airing_date = models.DateTimeField(null=True, blank=True)
    rating = models.CharField(max_length=128, null=True, blank=True)
    mal_id = models.CharField(max_length=128, null=True, blank=True)
    website = models.TextField(null=True, blank=True)
    total_episode = models.PositiveIntegerField(default=0)
    duration = models.PositiveIntegerField(default=0)
    is_publish = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'anime'

    def __str__(self):
        return '{}'.format(self.title)


class AnimeGenre(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    genre = models.ForeignKey('Genre', null=True, blank=True, on_delete=models.CASCADE)
    anime = models.ForeignKey('Anime', null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        db_table = 'anime_genre'


class MalAnime(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    mal_id = models.CharField(max_length=128, null=True, blank=True)
    log = models.CharField(max_length=128, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'mal_anime'
        verbose_name = 'Sync from MAL'

    def save(self):
        sync_anime.apply_async((self.mal_id, self.id))
        super(MalAnime, self).save()



