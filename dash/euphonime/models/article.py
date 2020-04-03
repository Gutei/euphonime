import uuid
from django.db import models
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.template.defaultfilters import slugify


class Article(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    image = models.ImageField(upload_to='anime/image', null=True, blank=True)
    title = models.CharField(max_length=128, default="-")
    content = RichTextUploadingField(blank=True, null=True, extra_plugins=['uploadimage'],)
    is_publish = models.BooleanField(default=False)
    slug = models.SlugField(max_length=512, blank=True, null=True,)
    prefix_id = models.SlugField(max_length=512, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'articles'

    def save(self, *args, **kwargs):
        uid = self.id.hex[:8]

        self.slug = slugify(self.title)
        self.prefix_id = '{}'.format(uid)

        super(Article, self).save(*args, **kwargs)