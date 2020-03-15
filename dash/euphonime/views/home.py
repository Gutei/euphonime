from django.shortcuts import render
from euphonime.models import Anime


def home(request):
    model = Anime
    template_name = 'euphonime/home.html'

    context = {
        'season_nime': model.objects.filter(is_publish=True)

    }
    return render(request, template_name, context)
