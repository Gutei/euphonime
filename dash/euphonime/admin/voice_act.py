from django.contrib import admin
from euphonime.models import VoiceAct

@admin.register(VoiceAct, site=admin.site)
class VoiceActAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)