import uuid
from django.db import models

class VoiceAct(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    image = models.ImageField(upload_to='seiyuu/image', null=True, blank=True)
    name = models.CharField(max_length=128, default="-")
    native_name = models.CharField(max_length=128, default="-")
    description = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'voice_acts'
        verbose_name = 'Voice Actress/Actor'