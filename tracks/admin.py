from django.contrib import admin
from .models import Track, TrackComment, TrackApiList


class TrackAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'track_id', 'created_at')


class TrackCommentAdmin(admin.ModelAdmin):
    list_display = ('track', 'user', 'content', 'created_at')


class TrackApiListAdmin(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(Track, TrackAdmin)
admin.site.register(TrackComment, TrackCommentAdmin)
admin.site.register(TrackApiList, TrackApiListAdmin)
