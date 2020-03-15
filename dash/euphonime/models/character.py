import uuid
from django.db import models


class Character(models.Model):

    MAIN = 1
    SUPPORT = 2

    ROLE = (
        (MAIN, 'Main'),
        (SUPPORT, 'Support')
    )

    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    image = models.ImageField(upload_to='character/image', null=True, blank=True, max_length=1500)
    image_url = models.CharField(null=True, blank=True, max_length=1500)
    name = models.CharField(max_length=128, default="-")
    native_name = models.CharField(max_length=128, default="-")
    role = models.PositiveIntegerField(choices=ROLE, null=True, blank=True)
    anime = models.ForeignKey('Anime', null=True, blank=True, on_delete=models.CASCADE)
    voice_act = models.ForeignKey('VoiceAct', null=True, blank=True, on_delete=models.PROTECT)
    mal_id = models.CharField(max_length=128, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'characters'

    def __str__(self):
        return '{}'.format(self.name)