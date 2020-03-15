from django.shortcuts import render
from euphonime.models import Anime


def anime(request, pk):
    model = Anime
    template_name = 'euphonime/anime.html'

    context = {
        'anime': model.objects.filter(id=pk).first()

    }
    return render(request, template_name, context)
