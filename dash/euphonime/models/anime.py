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
        id = self.mal_id
        url = "https://api.jikan.moe/v3/anime/{}".format(id)
        req = requests.get(url)
        
        status = "[FAILED][{}][{}]".format(id, req.status_code)
        self.log = status

        logger.debug('GET from {}'.format(url))
        logger.debug('{}, status={}'.format(url, status))

        if req.status_code == 200:
            json = req.json()

            logger.debug('GET ANIME {} SUCCESS, status={}'.format(json['title'], status))

            a = Anime.objects.filter(mal_id=id).first()
            if not a:
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

                anime.total_episode = 0 if not json['episodes'] else json['episodes']
                anime.airing_date = json['aired']['from']
                duration = re.findall(r'\d+', json['duration'])
                anime.duration = 0 if not duration else duration[0]
                anime.rating = json['rating']
                anime.is_publish = True
                anime.image_url = json['image_url']
                anime.description = json['synopsis']
                anime.mal_id = id

                anime.save()

                par_anime = anime

            else:
                a = Anime()
                a.title = json['title']
                a.native_title = json['title_japanese']
                a.english_title = json['title_english']

                if json['type'] == Anime.TYPE[0][1]:
                    a.type = 1
                elif json['type'] == Anime.TYPE[1][1]:
                    a.type = 2
                elif json['type'] == Anime.TYPE[2][1]:
                    a.type = 3
                elif json['type'] == Anime.TYPE[3][1]:
                    a.type = 4
                elif json['type'] == Anime.TYPE[4][1]:
                    a.type = 5

                a.total_episode = 0 if not json['episodes'] else json['episodes']
                a.airing_date = json['aired']['from']
                duration = re.findall(r'\d+', json['duration'])
                a.duration = 0 if not duration else duration[0]
                a.rating = json['rating']
                a.is_publish = True
                a.image_url = json['image_url']
                a.description = json['synopsis']
                a.mal_id = id

                try:
                    a.save()
                except Exception as e:
                    logger.debug('GET ANIME {} FAILED'.format(json['title']))

                par_anime = a

            status = "[ONLY ANIME SYNCHRONIZED][{}][{}]".format(id, req.status_code)

            chara_url = "{}/characters_staff".format(url)
            req_chara = requests.get(chara_url)
            if req_chara.status_code == 200:
                chara_json = req_chara.json()
                characters = chara_json['characters']
                for c in characters:
                    chara_name = ''
                    act = None
                    logger.debug('GET CHARACTER {} SUCCESS'.format(c['name']))
                    for v in c['voice_actors']:
                        if v['language'] == 'Japanese':
                            seiyuu_url = "https://api.jikan.moe/v3/person/{}/".format(v['mal_id'])
                            req_seiyuu = requests.get(seiyuu_url)
                            if req_seiyuu.status_code == 200:
                                logger.debug('GET CHARACTER {} SUCCESS'.format(v['name']))
                                seiyuu_json = req_seiyuu.json()
                                seiyuu, created = VoiceAct.objects.get_or_create(mal_id=v['mal_id'], name=v['name'],
                                                                                 given_name=seiyuu_json['given_name'],
                                                                                 family_name=seiyuu_json['family_name'],
                                                                                 image_url=seiyuu_json['image_url'],
                                                                                 description=seiyuu_json['about'],
                                                                                 birth_date=seiyuu_json['birthday'],)

                            else:
                                seiyuu, created = VoiceAct.objects.get_or_create(mal_id=v['mal_id'], name=v['name'],
                                                                                 image_url=v['image_url'])

                            chara_name = c['name']
                            act = seiyuu
                    if chara_name and chara_name != '':
                        if c['role'] == 'Main':
                            role = 1
                        else:
                            role = 2
                        chara_url = "https://api.jikan.moe/v3/character/{}/".format(c['mal_id'])
                        req_detail_chara = requests.get(chara_url)
                        detail_json = req_detail_chara.json()
                        logger.debug('ADD CHARACTER {} SUCCESS'.format(c['name']))
                        if req_detail_chara.status_code == 200:
                            chara, chara_created = Character.objects.get_or_create(mal_id=c['mal_id'], name=c['name'],
                                                                                   native_name=detail_json['name_kanji'],
                                                                                   image_url=detail_json['image_url'],
                                                                                   description=detail_json['about'],
                                                                                   anime=par_anime, voice_act=act,
                                                                                   role=role)


                        else:
                            chara, chara_created = Character.objects.get_or_create(mal_id=c['mal_id'], name=c['name'],
                                                                                   image_url=c['image_url'],
                                                                                   anime=par_anime, voice_act=act,
                                                                                   role=role)

                status = "[SUCCESS] Sync from MyAnimeList for {}, with title: {}.".format(id, anime.title)

            self.log = status
                
            
            super(MalAnime, self).save()



