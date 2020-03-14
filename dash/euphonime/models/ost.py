import uuid
from django.db import models


class OstAuthor(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=128, default="-")
    description = models.TextField(null=True, blank=True)
    icon = models.ImageField(upload_to='ost/author/icon', null=True, blank=True)

    class Meta:
        db_table = 'ost_authors'


class Ost(models.Model):

    OPENING_SONG = 1
    ENDING_SONG = 2
    INSERT_SONG = 3

    TYPE = (
        (OPENING_SONG, 'Opening Song'),
        (ENDING_SONG, 'Ending Song'),
        (INSERT_SONG, 'Insert Song'),
    )

    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=128, default="-")
    anime = models.ForeignKey('Anime', null=True, blank=True, on_delete=models.PROTECT)
    type = models.PositiveIntegerField(choices=TYPE, null=True, blank=True)
    author = models.ForeignKey('OstAuthor', null=True, blank=True, on_delete=models.PROTECT)
    lyric = models.TextField(null=True, blank=True)
    url = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'ost'
        verbose_name = 'Original Soundtrack'