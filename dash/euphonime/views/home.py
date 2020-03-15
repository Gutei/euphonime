from django.shortcuts import render
from euphonime.models import Anime


def home(request):
    anime = Anime.objects.filter(is_publish=True)
    template_name = 'euphonime/home.html'
    print(anime)

    context = {
        'season_nime': anime
    }
    return render(request, template_name, context)
