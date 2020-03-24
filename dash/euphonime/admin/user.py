from django.contrib import admin
from euphonime.models import ProfileUser, UserWatching, UserAnimeScore, UserPolls, UserMessage, UserPost

class ScoreInline(admin.TabularInline):
    model = UserAnimeScore
    extra = 1
    raw_id_fields = ('anime',)

class WatchingInline(admin.TabularInline):
    model = UserWatching
    extra = 1
    raw_id_fields = ('anime',)

class PollsInline(admin.TabularInline):
    model = UserPolls
    extra = 1
    raw_id_fields = ('anime',)

@admin.register(ProfileUser, site=admin.site)
class ProfileUserAdmin(admin.ModelAdmin):
    list_display = ('get_email', 'get_username', 'get_fullname','birth_date')
    search_fields = ('get_email', 'get_username',)
    inlines = [
        WatchingInline,
        ScoreInline,
        PollsInline,
    ]
    list_per_page = 10

    def get_email(self, obj):
        return obj.user.email
    get_email.admin_order_field = 'email'
    get_email.short_description = 'Email'

    def get_username(self, obj):
        return obj.user.username
    get_username.admin_order_field = 'username'
    get_username.short_description = 'Username'

    def get_fullname(self, obj):
        first_name = obj.user.first_name
        last_name = obj.user.last_name
        return '{} {}'.format(first_name, last_name)
    get_fullname.admin_order_field = 'fullname'
    get_fullname.short_description = 'Full Name'


@admin.register(UserMessage, site=admin.site)
class UserMessageAdmin(admin.ModelAdmin):
    list_display = ('get_email', 'message', 'created')
    search_fields = ('get_email',)
    list_per_page = 10

    def get_email(self, obj):
        return obj.user.user.email
    get_email.admin_order_field = 'email'
    get_email.short_description = 'Email'


@admin.register(UserPost, site=admin.site)
class UserPostAdmin(admin.ModelAdmin):
    list_display = ('get_email', 'created')
    search_fields = ('get_email',)
    list_filter = ('created',)
    list_per_page = 10

    def get_email(self, obj):
        return obj.user.user.email
    get_email.admin_order_field = 'user'
    get_email.short_description = 'User'