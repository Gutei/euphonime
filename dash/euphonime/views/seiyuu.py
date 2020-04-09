import random

from django.shortcuts import render
from euphonime.models import Anime, AnimeCharacter, Article, Season, AnimeSeason, UserPolls, UserWatching, UserAnimeScore, MetaGeneral, VoiceAct, Character,  MetaPage
from django.db.models import Avg, Sum
from django.views.decorators.cache import cache_page

def seiyuu(request, slug):
    seiyuu = VoiceAct.objects.filter(slug=slug).first()
    characters = Character.objects.filter(voice_act=seiyuu)
    meta = MetaPage.objects.filter(page=MetaPage.CHARACTER, ).exclude(
        meta_name__in=['title', 'description', 'og:image', 'og:title', 'og:description', 'keywords', 'og:url'])

    seiyuu.description = seiyuu.description.replace("\\n", "<br>")
    seiyuu.description = seiyuu.description.replace("\r", "")
    seiyuu.description = seiyuu.description.replace("\t", "")

    anime_characters = AnimeCharacter.objects.filter(character__in=characters)

    context = {
        'seiyuu': seiyuu,
        'characters': anime_characters,
        'meta': meta,
    }

    return render(request, 'euphonime/seiyuu/seiyuu.html', context)