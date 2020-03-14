import uuid
from django.db import models


class Character(models.Model):

    PROTAGONIST = 1
    ANTAGONIST = 2
    OTHER = 3

    ROLE = (
        (PROTAGONIST, 'Protagonis'),
        (ANTAGONIST, 'Antagonis'),
        (OTHER, 'Sampingan')
    )

    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    image = models.ImageField(upload_to='character/image', null=True, blank=True)
    name = models.CharField(max_length=128, default="-")
    native_name = models.CharField(max_length=128, default="-")
    role = models.PositiveIntegerField(choices=ROLE, null=True, blank=True)
    anime = models.ForeignKey('Anime', null=True, blank=True, on_delete=models.PROTECT)
    voice_act = models.ForeignKey('VoiceAct', null=True, blank=True, on_delete=models.PROTECT)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'characters'