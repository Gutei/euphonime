from django.utils.html import mark_safe
from django.contrib import admin
from euphonime.models import Anime, Character, Studio, Producer, AnimeStudio, AnimeProducer, AnimeGenre, MalAnime


class CharacterInline(admin.TabularInline):
    model = Character
    exclude = ('native_name', 'mal_id', 'image_url', 'description')
    raw_id_fields = ('voice_act',)
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
    list_display = ('title', 'get_image', 'is_publish', 'created','updated')
    search_fields = ('title',)
    list_filter = ('is_publish', 'created', 'updated')
    inlines = [
        AnimeGenreInline,
        CharacterInline,
        AnimeStudioInline,
        AnimeProducerInline,
    ]
    list_per_page = 10

    def get_image(self, obj):
        if obj.image:
            image = obj.image.url
            return mark_safe("<img src='{}' width='30'>".format(image))
        elif obj.image_url:
            image = obj.image_url
            return mark_safe("<img src='{}' width='30'>".format(image))

        return '-'

    get_image.admin_order_field = 'image'
    get_image.short_description = 'Image'

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
    list_display = ('id', 'log', 'created')
    search_fields = ('id', 'mal_id')
    list_filter = ('created',)
    exclude = ('log',)
    change_form_template = "admin/malanime/change_form.html"

@admin.register(Character, site=admin.site)
class CharacterAdmin(admin.ModelAdmin):
    list_display = ('get_image', 'role', 'anime', 'get_actor')
    search_fields = ('name', 'voice_act__name')
    raw_id_fields = ('voice_act', 'anime')
    list_per_page = 10

    def get_image(self, obj):
        if obj:
            if obj.image:
                image = obj.image.url
                return mark_safe("<img src='{}' width='30'> {}".format(image, obj.name))
            elif obj.image_url:
                image = obj.image_url
                return mark_safe("<img src='{}' width='30'> {}".format(image, obj.name))

        return '-'

    get_image.admin_order_field = 'image'
    get_image.short_description = 'Image'

    def get_actor(self, obj):
        if obj:
            if obj.voice_act.image:
                image = obj.voice_act.image.url
                return mark_safe("<img src='{}' width='30'> {}".format(image, obj.voice_act.name))
            elif obj.voice_act.image_url:
                image = obj.voice_act.image_url
                return mark_safe("<img src='{}' width='30'> {}".format(image, obj.voice_act.name))

        return '-'

    get_actor.admin_order_field = 'actor'
    get_actor.short_description = 'Voice actress/actor'