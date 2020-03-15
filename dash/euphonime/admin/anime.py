from django.contrib import admin
from euphonime.models import Anime, Character, Studio, Producer, AnimeStudio, AnimeProducer, AnimeGenre, MalAnime


class CharacterInline(admin.TabularInline):
    model = Character
    extra = 1

class AnimeStudioInline(admin.TabularInline):
    model = AnimeStudio
    extra = 1

class AnimeProducerInline(admin.TabularInline):
    model = AnimeProducer
    extra = 1

class AnimeGenreInline(admin.TabularInline):
    model = AnimeGenre
    extra = 1

@admin.register(Anime, site=admin.site)
class AnimeAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_publish', 'created','updated')
    search_fields = ('title',)
    list_filter = ('created', 'updated')
    inlines = [
        AnimeGenreInline,
        CharacterInline,
        AnimeStudioInline,
        AnimeProducerInline,
    ]

@admin.register(Studio, site=admin.site)
class StudioAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Producer, site=admin.site)
class ProducerAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(MalAnime, site=admin.site)
class MalAnimeAdmin(admin.ModelAdmin):
    list_display = ('id',)
    search_fields = ('id',)

@admin.register(Character, site=admin.site)
class CharacterAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)