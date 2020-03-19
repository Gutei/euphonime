from django.contrib import admin
from euphonime.models import Ost, OstAuthor

@admin.register(Ost, site=admin.site)
class OstAdmin(admin.ModelAdmin):
    list_display = ('title', 'anime', 'type')
    search_fields = ('title', 'anime')
    list_filter = ('type',)
    list_per_page = 10
    raw_id_fields = ('anime', 'author',)

@admin.register(OstAuthor, site=admin.site)
class OstAuthorAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('title',)
    list_per_page = 10