import uuid
from django.core.management.base import BaseCommand
from django.utils import timezone
from euphonime.models import MetaGeneral, MetaPage, Article, Anime, Character, VoiceAct, MetaPage
from django.template.defaultfilters import slugify

class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        seiyuu = VoiceAct.objects.all()

        for a in seiyuu:
            uid = a.id.hex[:4]
            a.slug = "{}-{}".format(uid, slugify(a.name))
            a.save()

        return None