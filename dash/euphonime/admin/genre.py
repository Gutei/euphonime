from django.contrib import admin
from euphonime.models import Genre


@admin.register(Genre, site=admin.site)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)