from django.contrib import admin
from .models import Track


class TrackAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'track_id')

admin.site.register(Track, TrackAdmin)