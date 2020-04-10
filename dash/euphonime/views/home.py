import random
import re
from django.shortcuts import render
from euphonime.models import Anime, Article, Season, AnimeSeason, UserPolls, UserWatching, UserAnimeScore, MetaGeneral, UserPost
from django.db.models import Avg, Sum
from django.views.decorators.cache import cache_page


# @cache_page(60 * 15)
def home(request):
    uagent = "{} {}".format(request.user_agent.browser.family, request.user_agent.browser.version_string)
    uos = "{} {}".format(request.user_agent.os.family, request.user_agent.os.version_string)

    ses_anime = Anime.objects.filter(is_publish=True)
    new_anime = Anime.objects.filter(is_publish=True).order_by('-updated')[:4]
    article = Article.objects.filter(is_publish=True).order_by('-updated')[:8]
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

    last_thread = UserPost.objects.all().order_by('-updated')[:4]

    ust_parse = []

    for u_p in last_thread:
        img = re.search('<img src="([^"]+)"'[4:], u_p.content)
        display_img = None
        img_thread_url = None
        no_prefix = None
        if img:
            display_img = img.group().strip('"')
            if display_img.split('"')[0] == " src=":
                no_prefix = display_img.split('"')[1]
                if no_prefix.split(':')[0] == 'https' or no_prefix.split(':')[0] == 'http':
                    img_thread_url = no_prefix
                else:
                    img_thread_url = None

        ust_parse.append({
            'id': u_p.id,
            'created': u_p.created,
            'content': u_p.content,
            'updated': u_p.updated,
            'img': None if not img_thread_url else img_thread_url,
            'obj': u_p,
        })

    context = {
        'season_nime': shuffle_ses_anime,
        'new_anime': new_anime,
        'article': article,
        'polls': result_polls,
        'meta': meta,
        'uagent': uagent,
        'uos': uos,
        'last_thread': ust_parse,
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
