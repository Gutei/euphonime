from django.contrib import admin
from euphonime.models import VoiceAct, SampleVoiceAct

class SampleVoiceActInline(admin.TabularInline):
    model = SampleVoiceAct
    extra = 1

@admin.register(VoiceAct, site=admin.site)
class VoiceActAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

    inlines = [
        SampleVoiceActInline,
    ]