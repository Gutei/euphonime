import uuid
from django.db import models


class Anime(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    image = models.ImageField(upload_to='anime/image', null=True, blank=True)
    title = models.CharField(max_length=128, default="-")
    native_title = models.CharField(max_length=128, default="-")
    description = models.TextField(null=True, blank=True)
    airing_date = models.DateTimeField(null=True, blank=True)
    genre = models.ForeignKey('Genre', null=True, blank=True, on_delete=models.PROTECT)
    website = models.TextField(null=True, blank=True)
    total_episode = models.PositiveIntegerField(default=0)
    duration = models.PositiveIntegerField(default=0)
    is_publish = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'anime'

    def __str__(self):
        return '{}'.format(self.title)