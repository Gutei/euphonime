from django.shortcuts import render
from euphonime.models import Anime, Article, Season, AnimeSeason, UserPolls, UserWatching, UserAnimeScore
from django.db.models import Avg, Sum


def home(request):
    ses_anime = Anime.objects.filter(is_publish=True)
    new_anime = Anime.objects.filter(is_publish=True).order_by('-updated')[:4]
    article = Article.objects.filter(is_publish=True).order_by('-updated')[:4]
    template_name = 'euphonime/home.html'
    this_sesason = Season.objects.filter(is_season=True).first()
    anime_season = ses_anime
    if this_sesason:
        ses_anime = []
        anime_season = AnimeSeason.objects.filter(season=this_sesason)
        for sa in anime_season:
            ses_anime.append(sa.anime)

    polls = []

    i = 1

    for s in anime_season:
        score = UserAnimeScore.objects.filter(anime=s.anime).aggregate(Avg('score'))
        polling = UserPolls.objects.filter(anime=s.anime).count()
        watch = UserWatching.objects.filter(anime=s.anime).count()
        polls.append({
            'number': i,
            'obj': s.anime,
            'polls': polling if polling < 999999 else '1000000+',
            'watch': watch if watch < 999999 else '1000000+',
            'score': '-' if not score['score__avg'] else score['score__avg'],
        })
        i += 1

    context = {
        'season_nime': ses_anime,
        'new_anime': new_anime,
        'article': article,
        'polls': polls,
    }
    return render(request, template_name, context)
