from django.core.management.base import BaseCommand
from django.utils import timezone
from euphonime.models import MetaGeneral, MetaPage, Article, Anime, Character
from django.template.defaultfilters import slugify

class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        articles = Article.objects.all()
        anime = Anime.objects.all()
        characters = Character.objects.all()

        for a in articles:
            a.slug = slugify(a.title)
            a.save()

        for an in anime:
            an.slug = slugify(an.title)
            an.save()

        for c in characters:
            c.slug = slugify(c.name)
            c.save()

        return None