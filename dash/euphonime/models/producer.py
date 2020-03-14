import uuid
from django.db import models


class Producer(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=128, default="-")
    description = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'producers'

class AnimeProducer(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    producer = models.ForeignKey('Producer', null=True, blank=True, on_delete=models.CASCADE)
    anime = models.ForeignKey('Anime', null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        db_table = 'anime_producers'