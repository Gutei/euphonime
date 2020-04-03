from django.contrib import admin
from euphonime.models import Article


@admin.register(Article, site=admin.site)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_publish', 'slug', 'created','updated')
    search_fields = ('title',)
    list_filter = ('created', 'updated')
    list_per_page = 10