from django.shortcuts import render
from euphonime.models import Anime, Article


def home(request):
    ses_anime = Anime.objects.filter(is_publish=True)
    new_anime = Anime.objects.filter(is_publish=True).order_by('-updated')[:6]
    article = Article.objects.filter(is_publish=True).order_by('-updated')[:4]
    template_name = 'euphonime/home.html'

    context = {
        'season_nime': ses_anime,
        'new_anime': new_anime,
        'article': article
    }
    return render(request, template_name, context)
