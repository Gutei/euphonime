from django.shortcuts import render
from euphonime.models import Anime, Character, AnimeGenre


def get_anime(request, pk, name):
    anime = Anime.objects.filter(id=pk).first()
    character = Character.objects.filter(anime=anime)
    genre = AnimeGenre.objects.filter(anime=anime)

    template_name = 'euphonime/anime.html'

    context = {
        'anime': anime,
        'character': character,
        'genre': genre
    }
    return render(request, template_name, context)

