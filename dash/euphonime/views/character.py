from django.db.models import Q
from django.core.paginator import Paginator
from django.db.models import Count
from django.shortcuts import render
from euphonime.models import Anime, Character, Quote, AnimeCharacter, MetaPage


def get_character(request, pk):
    character = Character.objects.filter(id=pk).first()
    quote = Quote.objects.filter(character=character)
    meta = MetaPage.objects.filter(page=MetaPage.CHARACTER,).exclude(meta_name__in=['title', 'description', 'og:image', 'og:title', 'og:description', 'keywords'])

    template_name = 'euphonime/character/get-character.html'

    anime = AnimeCharacter.objects.filter(character=character)

    context = {
        'character': character,
        'quotes': quote,
        'anime': anime,
        'meta': meta,
    }
    return render(request, template_name, context)


def list_character(request):
    template_name = 'euphonime/character/list-character.html'
    character = Character.objects.order_by('-updated')
    meta = MetaPage.objects.filter(page=MetaPage.CHARACTER, )

    chr = []
    for c in character:
        chr.append({
            'character': c,
            'anime_character': AnimeCharacter.objects.filter(character=c)
        })


    search = request.GET.get('search')
    if request.method == 'GET' and search:
        character = Character.objects.filter(Q(name__icontains=search)).order_by('name')
        chr = []
        for c in character:
            chr.append({
                'character': c,
                'anime_character': AnimeCharacter.objects.filter(character=c)
            })

    paginator = Paginator(chr, 10)  # Show 25 contacts per page
    page = request.GET.get('page')
    characters_page = paginator.get_page(page)


    context = {
        'characters': characters_page,
        'meta': meta,
    }
    return render(request, template_name, context)
