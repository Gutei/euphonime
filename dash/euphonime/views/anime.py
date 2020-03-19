from django.db.models import Q
from django.core.paginator import Paginator
from django.shortcuts import render
from euphonime.models import Anime, Character, AnimeGenre


def get_anime(request, pk):
    anime = Anime.objects.filter(id=pk).first()
    character = Character.objects.filter(anime=anime)
    genre = AnimeGenre.objects.filter(anime=anime)

    template_name = 'euphonime/anime/get-anime.html'

    context = {
        'anime': anime,
        'character': character,
        'genre': genre
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
