import logging
import re
import requests
# Create your tasks here

logger = logging.getLogger(__name__)

from euphonime.models import Anime, Character, VoiceAct, MalAnime, AnimeCharacter


def get_anime(mal_id, task_id):
    id = mal_id

    exist_anime = Anime.objects.filter(mal_id=id).first()
    if exist_anime:
        logger.debug('[----ANIME EXSIST----]'.format(id))
        get_chara(id, exist_anime)
        return None

    logger.debug('===========STARTING SYNC FOR MAL ID {}============'.format(id))
    url = "https://api.jikan.moe/v3/anime/{}".format(id)
    req = requests.get(url)

    status = "[{}][{}]".format(id, req.status_code)

    logger.debug('GET from {}'.format(url))
    logger.debug('{}, status={}'.format(url, status))

    if req.status_code == 200:
        json = req.json()

        logger.debug('GET ANIME {} SUCCESS, status={}'.format(json['title'], req.status_code))

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

            get_chara(id, par_anime)

    return None


def get_chara(mal_id, par_anime):
    id = mal_id

    logger.debug('===========STARTING SYNC CHARACTER FROM MAL ID {}============'.format(id))
    url = "https://api.jikan.moe/v3/anime/{}".format(id)

    chara_url = "{}/characters_staff".format(url)
    req_chara = requests.get(chara_url)
    if req_chara.status_code == 200:
        chara_json = req_chara.json()
        characters = chara_json['characters']
        for c in characters:
            chara_name = ''
            clr_chara = Character.objects.filter(mal_id=c['mal_id'])
            clr_chara.delete()
            existed_chara = Character.objects.filter(mal_id=c['mal_id']).first()
            act = None
            logger.debug('SYNC CHARACTER {}'.format(c['name']))
            for v in c['voice_actors']:
                if v['language'] == 'Japanese':
                    seiyuu_url = "https://api.jikan.moe/v3/person/{}/".format(v['mal_id'])
                    req_seiyuu = requests.get(seiyuu_url)
                    if req_seiyuu.status_code == 200:
                        logger.debug('GET SEIYUU {} FOR CHARACTER {} SUCCESS'.format(v['name'], c['name']))
                        seiyuu_json = req_seiyuu.json()
                        seiyuu, created = VoiceAct.objects.get_or_create(mal_id=v['mal_id'], name=v['name'],
                                                                         given_name=seiyuu_json['given_name'],
                                                                         family_name=seiyuu_json['family_name'],
                                                                         image_url=seiyuu_json['image_url'],
                                                                         description=seiyuu_json['about'],
                                                                         birth_date=seiyuu_json['birthday'], )

                    else:
                        seiyuu, created = VoiceAct.objects.get_or_create(mal_id=v['mal_id'], name=v['name'],
                                                                         image_url=v['image_url'])

                    chara_name = c['name']
                    act = seiyuu


            if not existed_chara:
                if chara_name and chara_name != '':
                    if c['role'] == 'Main':
                        role = 1
                    else:
                        role = 2
                    chara_url = "https://api.jikan.moe/v3/character/{}/".format(c['mal_id'])
                    req_detail_chara = requests.get(chara_url)
                    logger.debug('ADD CHARACTER {} SUCCESS'.format(c['name']))
                    if req_detail_chara.status_code == 200:
                        detail_json = req_detail_chara.json()

                        chara = Character(mal_id=c['mal_id'], name=c['name'],
                                                                native_name=detail_json['name_kanji'],
                                                                image_url=detail_json['image_url'],
                                                                description=detail_json['about'],
                                                                voice_act=act,
                                                                role=role)
                        chara.save()

                        anime = par_anime
                        char_anime = AnimeCharacter(character=chara, anime=anime)
                        char_anime.save()


                    else:
                        Character.objects.update(mal_id=c['mal_id'], name=c['name'],
                                                 image_url=c['image_url'],
                                                 voice_act=act,
                                                 role=role)

                        chara = Character.objects.filter(character__mal_id=c['mal_id']).first()

                        anime = par_anime
                        char_anime = AnimeCharacter(character=chara, anime=anime)
                        char_anime.save()



        status = "[SUCCESS] Sync from MyAnimeList for {}, with title: {}.".format(id, par_anime.title)

    return None