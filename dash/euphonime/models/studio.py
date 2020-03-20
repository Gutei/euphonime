import uuid
from django.db import models


class Studio(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=128, default="-")
    description = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'studios'

    def __str__(self):
        return "{}".format(self.name)


class AnimeStudio(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    studio = models.ForeignKey('Studio', null=True, blank=True, on_delete=models.CASCADE)
    anime = models.ForeignKey('Anime', null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        db_table = 'anime_studios'

    def __str__(self):
        return "{} - {}".format(self.studio.name, self.anime.title)