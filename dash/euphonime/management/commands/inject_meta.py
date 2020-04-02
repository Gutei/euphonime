from django.core.management.base import BaseCommand
from django.utils import timezone
from euphonime.models import MetaGeneral, MetaPage

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        list_meta = [
            {
                'meta_name': 'title',
                'value': '<title>EuphoNime - Informasi Anime & Komunitas Otaku Indonesia</title>'
            },
            {
                'meta_name': 'description',
                'value': '<meta name="description" content="EuphoNime adalah media, database anime, dan situs komunitas untuk penggemar anime yang dapat saling berinteraksi di Indonesia." />'
            },
            {
                'meta_name': 'keywords',
                'value': '<meta name="keywords" content="berita anime, info anime, info karakter anime, berita otaku, forum otaku"/>'
            },
            {
                'meta_name': 'author',
                'value': '<meta name="author" content="EuphoNime">'
            },
            {
                'meta_name': 'coverage',
                'value': '<meta name="coverage" content="Worldwide">'
            },
            {
                'meta_name': 'distribution',
                'value': '<meta name="distribution" content="Global">'
            },
            {
                'meta_name': 'og:title',
                'value': '<meta property="og:title" content="EuphoNime"/>'
            },
            {
                'meta_name': 'og:description',
                'value': '<meta property="og:description" content="EuphoNime adalah media, database anime, dan situs komunitas untuk penggemar anime yang dapat saling berinteraksi di Indonesia.">'
            },
            {
                'meta_name': 'og:type',
                'value': '<meta property="og:type" content="website" />'
            },
            {
                'meta_name': 'og:url',
                'value': '<meta property="og:url" content="https://euphonime.com/" />'
            },
            {
                'meta_name': 'og:site_name',
                'value': '<meta property="og:site_name" content="EuphoNime.com" />'
            },
            {
                'meta_name': 'og:image',
                'value': '<meta property="og:image" content="https://euphonime.com/static/euphonime/img/euphonime-og.jpg">'
            },
        ]

        for meta in list_meta:
            m = MetaGeneral.objects.filter(meta_name=meta['meta_name']).first()
            if not m:
                m = MetaGeneral(meta_name=meta['meta_name'], value=meta['value'])
                m.save()

        pages = [1,2,3,4]

        for p in pages:

            if p == 1:
                title = 'Anime'
            if p == 2:
                title = 'Articles'
            if p == 3:
                title = 'Characters'
            if p == 4:
                title = 'Quotes'

            list_meta_page = [
                {
                    'meta_name': 'title',
                    'page': p,
                    'value': '<title>{} - EuphoNime</title>'.format(title)
                },
                {
                    'meta_name': 'description',
                    'page': p,
                    'value': '<meta name="description" content="EuphoNime adalah media, database anime, dan situs komunitas untuk penggemar anime yang dapat saling berinteraksi di Indonesia." />'
                },
                {
                    'meta_name': 'keywords',
                    'page': p,
                    'value': '<meta name="keywords" content="berita anime, info anime, info karakter anime, berita otaku, forum otaku"/>'
                },
                {
                    'meta_name': 'author',
                    'page': p,
                    'value': '<meta name="author" content="EuphoNime">'
                },
                {
                    'meta_name': 'coverage',
                    'page': p,
                    'value': '<meta name="coverage" content="Worldwide">'
                },
                {
                    'meta_name': 'distribution',
                    'page': p,
                    'value': '<meta name="distribution" content="Global">'
                },
                {
                    'meta_name': 'og:title',
                    'page': p,
                    'value': '<meta property="og:title" content="{} - EuphoNime"/>'.format(title)
                },
                {
                    'meta_name': 'og:description',
                    'page': p,
                    'value': '<meta property="og:description" content="EuphoNime adalah media, database anime, dan situs komunitas untuk penggemar anime yang dapat saling berinteraksi di Indonesia.">'
                },
                {
                    'meta_name': 'og:type',
                    'page': p,
                    'value': '<meta property="og:type" content="website" />'
                },
                {
                    'meta_name': 'og:url',
                    'page': p,
                    'value': '<meta property="og:url" content="https://euphonime.com/" />'
                },
                {
                    'meta_name': 'og:site_name',
                    'page': p,
                    'value': '<meta property="og:site_name" content="EuphoNime.com" />'
                },
                {
                    'meta_name': 'og:image',
                    'page': p,
                    'value': '<meta property="og:image" content="https://euphonime.com/static/euphonime/img/euphonime-og.jpg">'
                },
            ]

            for meta in list_meta_page:
                m = MetaPage.objects.filter(meta_name=meta['meta_name'], page=meta['page']).first()
                if not m:
                    m = MetaPage(meta_name=meta['meta_name'], page=meta['page'], value=meta['value'])
                    m.save()

        return None