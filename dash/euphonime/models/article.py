import uuid
from django.db import models
from ckeditor.fields import RichTextField

class Article(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    image = models.ImageField(upload_to='anime/image', null=True, blank=True)
    title = models.CharField(max_length=128, default="-")
    content = RichTextField(blank=True, null=True)
    is_publish = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'articles'