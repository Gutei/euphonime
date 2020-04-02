import uuid
from django.db import models

class MetaGeneral(models.Model):

    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    meta_name = models.CharField(max_length=128, default="-")
    value = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'meta_generals'


class MetaPage(models.Model):

    ANIME = 1
    ARTICLE = 2
    CHARACTER = 3
    QUOTE = 4

    PAGES = (
        (ANIME, 'Anime'),
        (ARTICLE, 'Article'),
        (CHARACTER, 'Character'),
        (QUOTE, 'Quote'),
    )

    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    meta_name = models.CharField(max_length=128, default="-")
    page = models.PositiveSmallIntegerField(choices=PAGES, null=True, blank=True)
    value = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'meta_pages'