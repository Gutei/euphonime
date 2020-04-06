import random
from django.shortcuts import render
from euphonime.models import Anime, Article, Season, AnimeSeason, UserPolls, UserWatching, UserAnimeScore, MetaGeneral
from django.db.models import Avg, Sum
from django.views.decorators.cache import cache_page


# @cache_page(60 * 15)
def home(request):
    ses_anime = Anime.objects.filter(is_publish=True)
    new_anime = Anime.objects.filter(is_publish=True).order_by('-updated')[:4]
    article = Article.objects.filter(is_publish=True).order_by('-updated')[:4]
    template_name = 'euphonime/home.html'
    meta = MetaGeneral.objects.all()
    this_sesason = Season.objects.filter(is_season=True).first()
    polls = []
    result_polls = []
    anime_season = ses_anime
    if this_sesason:
        ses_anime = []
        anime_season = AnimeSeason.objects.filter(season=this_sesason)
        for sa in anime_season:
            ses_anime.append(sa.anime)

        i = 1

        for s in anime_season:
            score = UserAnimeScore.objects.filter(anime=s.anime).aggregate(Avg('score'))
            polling = UserPolls.objects.filter(anime=s.anime).count()
            watch = UserWatching.objects.filter(anime=s.anime).count()
            user_poll = UserPolls.objects.filter(anime=s.anime).count()
            polls.append({
                'number': i,
                'obj': s.anime,
                # 'polls': polling,
                'watch': watch,
                'score': 0 if not score['score__avg'] else score['score__avg'],
                'polls': user_poll,
            })
            i += 1

        ranking = 1
        sorted_polls = sorted(polls, key = lambda i : i['score'], reverse=True)
        for s_polls in sorted_polls:
            s_polls['number'] = ranking
            result_polls.append(s_polls)
            ranking += 1

    if len(ses_anime) > 10:
        ses_anime_random_sample = 10
        shuffle_ses_anime = random.sample(set(ses_anime), ses_anime_random_sample)
    else:
        shuffle_ses_anime = ses_anime

    context = {
        'season_nime': shuffle_ses_anime,
        'new_anime': new_anime,
        'article': article,
        'polls': result_polls,
        'meta': meta,
    }
    return render(request, template_name, context)


def robots_txt(request):
    anime = Anime.objects.all()
    an = []
    for a in anime:
        an.append(a.id)

    context = {
        'anime_id': an,
    }

    return render(request, 'euphonime/robots.txt', context, content_type="text/plain")

def bing_site(request):
    return render(request, 'euphonime/BingSiteAuth.xml', content_type="text/xml")
