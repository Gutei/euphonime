from django.core.paginator import Paginator
from django.db.models import Count
from django.shortcuts import render
from euphonime.models import Anime, Character, AnimeGenre, Quote


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


def list_quote(request):
    template_name = 'euphonime/quote/list-quote.html'

    quote = Quote.objects.order_by('-updated')
    paginator = Paginator(quote, 10)  # Show 25 contacts per page
    page = request.GET.get('page')
    quote_page = paginator.get_page(page)

    context = {
        'quotes': quote_page,
    }
    return render(request, template_name, context)
