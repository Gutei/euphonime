from django.db.models import Q
from django.core.paginator import Paginator
from django.shortcuts import render
from euphonime.models import Anime, Character, AnimeGenre, Quote, UserAnimeScore, ProfileUser,Ost
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required


def get_anime(request, pk):
    anime = Anime.objects.filter(id=pk).first()
    character = Character.objects.filter(anime=anime)
    genre = AnimeGenre.objects.filter(anime=anime)
    quote = Quote.objects.filter(character__anime=anime).order_by('-updated')
    ost = Ost.objects.filter(anime=anime).order_by('-updated')

    template_name = 'euphonime/anime/get-anime.html'

    user_rate = None

    if not request.user.is_anonymous:
        profile = ProfileUser.objects.filter(user=request.user).first()
        if profile:
            user_rate = UserAnimeScore.objects.filter(user=profile, anime=anime).first()

    rating_counter_1 = UserAnimeScore.objects.filter(anime=anime, score=1).count()
    rating_counter_2 = UserAnimeScore.objects.filter(anime=anime, score=2).count()
    rating_counter_3 = UserAnimeScore.objects.filter(anime=anime, score=3).count()
    rating_counter_4 = UserAnimeScore.objects.filter(anime=anime, score=4).count()
    rating_counter_5 = UserAnimeScore.objects.filter(anime=anime, score=5).count()
    rating_counter_6 = UserAnimeScore.objects.filter(anime=anime, score=6).count()
    rating_counter_7 = UserAnimeScore.objects.filter(anime=anime, score=7).count()
    rating_counter_8 = UserAnimeScore.objects.filter(anime=anime, score=8).count()
    rating_counter_9 = UserAnimeScore.objects.filter(anime=anime, score=9).count()
    rating_counter_10 = UserAnimeScore.objects.filter(anime=anime, score=10).count()

    context = {
        'anime': anime,
        'character': character,
        'genre': genre,
        'quotes': quote,
        'ost': ost,
        'user_rate': user_rate,
        'rating_counter_1': rating_counter_1,
        'rating_counter_2': rating_counter_2,
        'rating_counter_3': rating_counter_3,
        'rating_counter_4': rating_counter_4,
        'rating_counter_5': rating_counter_5,
        'rating_counter_6': rating_counter_6,
        'rating_counter_7': rating_counter_7,
        'rating_counter_8': rating_counter_8,
        'rating_counter_9': rating_counter_9,
        'rating_counter_10': rating_counter_10,
    }
    return render(request, template_name, context)


def list_anime(request):
    template_name = 'euphonime/anime/list-anime.html'
    animes = Anime.objects.filter(is_publish=True).order_by('title')

    search = request.GET.get('search')
    if request.method == 'GET' and search:
        animes = Anime.objects.filter(Q(title__icontains=search)).order_by('-updated')

    paginator = Paginator(animes, 15)  # Show 25 contacts per page
    page = request.GET.get('page')
    animes_page = paginator.get_page(page)
    context = {
        'animes': animes_page,
    }
    return render(request, template_name, context)


@login_required
def save_rate(request, anime_id, rate):
    profile = ProfileUser.objects.filter(user=request.user).first()
    anime = Anime.objects.filter(id=anime_id).first()

    if not profile:
        return redirect(reverse('login'))

    user_rate = UserAnimeScore.objects.filter(user=profile, anime=anime).first()

    if user_rate:
        return redirect(reverse('anime', args=[anime.id, ]))

    user_rate = UserAnimeScore(user=profile, anime=anime, score=rate)
    user_rate.save()

    return redirect(reverse('anime', args=[anime.id, ]))
