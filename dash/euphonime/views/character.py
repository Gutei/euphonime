from django.core.paginator import Paginator
from django.db.models import Count
from django.shortcuts import render
from euphonime.models import Anime, Character,  Quote


def get_character(request, pk):
    character = Character.objects.filter(id=pk).first()
    quote = Quote.objects.filter(character=character)

    template_name = 'euphonime/character/get-character2.html'

    context = {
        'character': character,
        'quotes':quote
    }
    return render(request, template_name, context)


def list_character(request):
    template_name = 'euphonime/character/list-character.html'
    character = Character.objects.all()
    paginator = Paginator(character, 10)  # Show 25 contacts per page
    page = request.GET.get('page')
    characters_page = paginator.get_page(page)

    context = {
        'characters': characters_page,
    }
    return render(request, template_name, context)
