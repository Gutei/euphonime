from django.utils.html import mark_safe
from django.contrib import admin
from euphonime.models import (Anime, Character, Studio, Producer, AnimeStudio, AnimeProducer, AnimeGenre, MalAnime,
                              Quote, Season, AnimeSeason, AnimeCharacter, UserAnimeReview)
from euphonime.tasks import sync_anime

class CharacterInline(admin.TabularInline):
    model = AnimeCharacter
    raw_id_fields = ('character',)
    extra = 1

class AnimeSeasonInline(admin.TabularInline):
    model = AnimeSeason
    extra = 1
    raw_id_fields = ('anime',)

class QuoteInline(admin.TabularInline):
    model = Quote
    extra = 1

class AnimeStudioInline(admin.TabularInline):
    model = AnimeStudio
    extra = 1
    raw_id_fields = ('studio',)

class AnimeProducerInline(admin.TabularInline):
    model = AnimeProducer
    extra = 1
    raw_id_fields = ('producer',)

class AnimeGenreInline(admin.TabularInline):
    model = AnimeGenre
    extra = 1

@admin.register(Anime, site=admin.site)
class AnimeAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_image', 'is_publish', 'created', 'updated')
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

    def save_model(self, request, obj, form, change):
        # custom stuff here
        if obj.mal_id == "*":
            ac = AnimeCharacter.objects.all()
            c = Character.objects.all()
            ac.delete()
            c.delete()
            a = Anime.objects.all()
            list_a = []
            for la in a:
                list_a.append(la.mal_id)

            a = Anime.objects.filter(mal_id__in=list_a)
            a.delete()
            for sync in list_a:
                sync_anime.apply_async((sync, obj.id))
        else:
            sync_anime.apply_async((obj.mal_id, obj.id))
        super().save_model(request, obj, form, change)

@admin.register(Character, site=admin.site)
class CharacterAdmin(admin.ModelAdmin):
    list_display = ('get_image', 'role', 'get_anime', 'get_actor')
    search_fields = ('name', 'voice_act__name')
    raw_id_fields = ('voice_act',)
    list_per_page = 10

    inlines = [
        QuoteInline,
    ]

    def get_anime(self, obj):
        text = ""
        if obj:
            ac = AnimeCharacter.objects.filter(character=obj)
            if ac:
                for a in ac:
                    title = a.anime.title
                    res = "{}{},".format(text, title)
                    text = "{}".format(res)

                return text

        return '-'

    get_anime.admin_order_field = 'anime'
    get_anime.short_description = 'Anime(s)'

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
            if obj.voice_act:
                if obj.voice_act.image:
                    image = obj.voice_act.image.url
                    return mark_safe("<img src='{}' width='30'> {}".format(image, obj.voice_act.name))
                elif obj.voice_act.image_url:
                    image = obj.voice_act.image_url
                    return mark_safe("<img src='{}' width='30'> {}".format(image, obj.voice_act.name))

        return '-'

    get_actor.admin_order_field = 'actor'
    get_actor.short_description = 'Voice actress/actor'


@admin.register(Quote, site=admin.site)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ('get_image', 'get_anime', 'quote')
    search_fields = ('character__name', 'quote')
    raw_id_fields = ('character',)
    list_per_page = 10

    def get_anime(self, obj):
        if obj:
            if obj.character:
                anime_character = AnimeCharacter.objects.filter(character=obj.character).first()
                a = anime_character.anime.title
                return "{}".format(a)
        return '-'

    def get_image(self, obj):
        if obj:
            if obj.character.image:
                image = obj.character.image.url
                return mark_safe("<img src='{}' width='30'> {}".format(image, obj.character.name))
            elif obj.character.image_url:
                image = obj.character.image_url
                return mark_safe("<img src='{}' width='30'> {}".format(image, obj.character.name))

        return '-'

    get_image.admin_order_field = 'image'
    get_image.short_description = 'Image'


@admin.register(Season, site=admin.site)
class SeasonAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_season', 'created')
    search_fields = ('name',)
    list_filter = ('created', 'is_season',)
    list_editable = ('is_season',)

    inlines = [
        AnimeSeasonInline,
    ]

    def save_model(self, request, obj, form, change):

        if change:
            season = Season.objects.filter(is_season=True).first()

            if season:
                season.is_season = False
                season.save()

        super().save_model(request, obj, form, change)

# @admin.register(UserAnimeReview, site=admin.site)
# class UserAnimeReviewAdmin(admin.ModelAdmin):
#     list_display = ('get_user', 'anime', 'created', 'updated',)
#     search_fields = ('user__username', 'user__email', 'anime__title',)
#     list_filter = ('created', 'updated',)
#
#     def get_user(self, obj):
#         user = obj.user.user.email
#
#         return '{}'.format(user)
#
#     get_user.admin_order_field = 'user'
#     get_user.short_description = 'User'