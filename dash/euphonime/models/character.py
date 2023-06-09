import uuid
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.template.defaultfilters import slugify


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
    native_name = models.CharField(max_length=128, null=True, blank=True)
    description = RichTextUploadingField(null=True, blank=True, extra_plugins=['uploadimage'])
    role = models.PositiveIntegerField(choices=ROLE, null=True, blank=True)
    voice_act = models.ForeignKey('VoiceAct', null=True, blank=True, on_delete=models.PROTECT)
    mal_id = models.CharField(max_length=128, null=True, blank=True)
    slug = models.SlugField(max_length=512, null=True, blank=True)
    prefix_id = models.SlugField(max_length=512, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'characters'

    def __str__(self):
        return '{}'.format(self.name)

    def save(self, *args, **kwargs):

        uid = self.id.hex[:8]

        self.slug = slugify(self.name)
        self.prefix_id = '{}'.format(uid)

        super(Character, self).save(*args, **kwargs)


class AnimeCharacter(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    character = models.ForeignKey('Character', null=True, blank=True, on_delete=models.CASCADE)
    anime = models.ForeignKey('Anime', null=True, blank=True, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'anime_characters'

    def __str__(self):
        return '{} in anime {}'.format(self.character.name, self.anime.title)


class Quote(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    character = models.ForeignKey('Character', null=True, blank=True, on_delete=models.CASCADE)
    quote = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'quotes'