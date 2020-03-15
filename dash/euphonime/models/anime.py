import os
import re
import requests
import uuid
from django.db import models
from django.core.files import File
from .character import Character
from .voice_act import VoiceAct


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
    description = models.TextField(null=True, blank=True)
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
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'mal_anime'
        verbose_name = 'Upload from MAL'

    def save(self):
        id = self.mal_id
        url = "https://api.jikan.moe/v3/anime/{}".format(id)
        req = requests.get(url)

        if req.status_code == 200:
            json = req.json()

            anime = Anime()
            anime.title = json['title']
            anime.native_title = json['title_japanese']
            anime.english_title = json['title_english']

            if json['type'] == Anime.TYPE[0][1]:
                anime.type = 1
            elif json['type'] == Anime.TYPE[1][1]:
                anime.type = 2
            elif json['type'] == Anime.TYPE[2][1]:
                anime.type = 3
            elif json['type'] == Anime.TYPE[3][1]:
                anime.type = 4
            elif json['type'] == Anime.TYPE[4][1]:
                anime.type = 5

            anime.total_episode = json['episodes']
            anime.airing_date = json['aired']['from']
            duration = re.findall(r'\d+', json['duration'])
            anime.duration = duration[0]
            anime.rating = json['rating']
            anime.is_publish = True
            anime.image_url = json['image_url']

            anime.save()

            chara_url = "{}/characters_staff".format(url)
            req_chara = requests.get(chara_url)
            if req_chara.status_code == 200:
                chara_json = req_chara.json()
                characters = chara_json['characters']
                for c in characters:
                    chara_name = ''
                    act = None
                    for v in c['voice_actors']:
                        if v['language'] == 'Japanese':
                            seiyuu, created = VoiceAct.objects.get_or_create(mal_id=v['mal_id'], name=v['name'], image_url=v['image_url'])
                            chara_name = c['name']
                            act = seiyuu
                    if chara_name and chara_name != '':
                        chara, chara_created = Character.objects.get_or_create(mal_id=c['mal_id'], name=c['name'], image_url=c['image_url'], anime=anime, voice_act=act)

            super(MalAnime, self).save()



