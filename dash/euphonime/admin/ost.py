from django.contrib import admin
from euphonime.models import Ost, OstAuthor

@admin.register(Ost, site=admin.site)
class Ostdmin(admin.ModelAdmin):
    list_display = ('title', 'anime', 'type')
    search_fields = ('title', 'anime')
    list_filter = ('type',)

@admin.register(OstAuthor, site=admin.site)
class OstAuthorAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('title',)