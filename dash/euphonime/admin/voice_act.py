from django.utils.html import mark_safe
from django.contrib import admin
from euphonime.models import VoiceAct, SampleVoiceAct

class SampleVoiceActInline(admin.TabularInline):
    model = SampleVoiceAct
    extra = 1

@admin.register(VoiceAct, site=admin.site)
class VoiceActAdmin(admin.ModelAdmin):
    list_display = ('name', 'birth_date', 'given_name', 'family_name', 'get_image')
    search_fields = ('name',)

    inlines = [
        SampleVoiceActInline,
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