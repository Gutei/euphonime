from django.contrib import admin
from euphonime.models import MetaGeneral, MetaPage


@admin.register(MetaGeneral, site=admin.site)
class MetaGeneralAdmin(admin.ModelAdmin):
    list_display = ('meta_name', 'value')
    search_fields = ('meta_name', 'value')
    list_per_page = 100



@admin.register(MetaPage, site=admin.site)
class MetaPageAdmin(admin.ModelAdmin):
    list_display = ('meta_name', 'page', 'value')
    search_fields = ('meta_name', 'page', 'value')
    list_filter = ('meta_name', 'page',)
    list_per_page = 100