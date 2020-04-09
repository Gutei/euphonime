import uuid
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.template.defaultfilters import slugify

class VoiceAct(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    image = models.ImageField(upload_to='seiyuu/image', null=True, blank=True, max_length=1500)
    image_url = models.CharField(null=True, blank=True, max_length=1500)
    name = models.CharField(max_length=128, default="-")
    given_name = models.CharField(max_length=128, null=True, blank=True, )
    family_name = models.CharField(max_length=128, null=True, blank=True, )
    birth_date = models.DateTimeField(null=True, blank=True,)
    description = RichTextUploadingField(null=True, blank=True, extra_plugins=['uploadimage'])
    mal_id = models.CharField(max_length=128, null=True, blank=True)
    slug = models.SlugField(max_length=512, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'voice_acts'
        verbose_name = 'Voice Actress/Actor'

    def __str__(self):
        return '{}'.format(self.name)

    def save(self, *args, **kwargs):
        uid = self.id.hex[:4]

        self.slug = "{}-{}".format(uid, slugify(self.name))

        super(VoiceAct, self).save(*args, **kwargs)


class SampleVoiceAct(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    seiyuu = models.ForeignKey('VoiceAct', null=True, blank=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=128, null=True, blank=True)
    audio = models.FileField(upload_to='seiyuu/audio', max_length=100, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'voice_act_samples'