import uuid
from django.db import models

class Genre(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=128, default="-")
    icon = models.ImageField(upload_to='genre/icon', null=True, blank=True)

    class Meta:
        db_table = 'genres'

    def __str__(self):
        return '{}'.format(self.title)