from django.db.models import Q
from django.core.paginator import Paginator
from django.shortcuts import render
from euphonime.models import (Anime, Character, AnimeGenre, Quote, UserAnimeScore, ProfileUser, UserWatching,
                              AnimeCharacter, Ost, UserPolls, AnimeStudio, Studio)
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required


def get_anime(request, pk):
    anime = Anime.objects.filter(id=pk).first()
    anime_character = AnimeCharacter.objects.filter(anime=anime)
    characters = []
    for ac in anime_character:
        characters.append(ac.character)

    genre = AnimeGenre.objects.filter(anime=anime)

    quote = Quote.objects.filter(character__in=characters).order_by('-updated')

    ost = Ost.objects.filter(anime=anime)

    status = "Status belum Ada"

    template_name = 'euphonime/anime/get-anime.html'

    user_rate = None

    if not request.user.is_anonymous:
        profile = ProfileUser.objects.filter(user=request.user).first()
        if profile:
            user_rate = UserAnimeScore.objects.filter(user=profile, anime=anime).first()
            user_status = UserWatching.objects.filter(user=profile, anime=anime).first()
            if user_status:
                if user_status.status == UserWatching.WATCHING:
                    status = 'Status saat ini: Sedang ditonton'
                elif user_status.status == UserWatching.FINISHED_WATCHING:
                    status = 'Status saat ini: Selesai ditonton'
                elif user_status.status == UserWatching.HOLDING:
                    status = 'Status saat ini: Menunda untuk ditonton'
                elif user_status.status == UserWatching.STOP_WATCHING:
                    status = 'Status saat ini: Tidak melanjutkan menonton'
                else:
                    status = 'Status saat ini: -'

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

    studios = AnimeStudio.objects.filter(anime=anime)

    context = {
        'anime': anime,
        'character': characters,
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
        'status': status,
        'studios': studios,
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

    if request.method == "GET":
        return redirect(reverse('anime', args=[anime.id, ]))

    id = request.POST.get('id')
    val = request.POST.get('rate')

    anime = Anime.objects.filter(id=id).first()

    if not profile:
        return redirect(reverse('login'))

    user_rate = UserAnimeScore.objects.filter(user=profile, anime=anime).first()

    if user_rate:
        return redirect(reverse('anime', args=[anime.id, ]))

    user_rate = UserAnimeScore(user=profile, anime=anime, score=val)
    user_rate.save()

    user_poll = UserPolls(user=profile, anime=anime, poll=True)
    user_poll.save()

    return redirect(reverse('anime', args=[anime.id, ]))


@login_required
def save_watching(request, anime_id):
    profile = ProfileUser.objects.filter(user=request.user).first()
    anime = Anime.objects.filter(id=anime_id).first()

    if request.method == 'GET':
        return redirect(reverse('anime', args=[anime.id, ]))
    elif request.method == 'POST':
        if not profile:
            return redirect(reverse('login'))

        user_watching = UserWatching.objects.filter(user=profile, anime=anime).first()
        if request.POST.get('status') and request.POST.get('status') != "-":
            if user_watching:
                user_watching.status = int(request.POST.get('status'))
                user_watching.save()
            else:
                user_watching = UserWatching(user=profile, anime=anime, status=int(request.POST.get('status')))
                user_watching.save()

    return redirect(reverse('anime', args=[anime.id, ]))
