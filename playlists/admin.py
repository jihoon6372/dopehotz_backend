from django.contrib import admin

from .models import PlayList, PlayListGroup

class PlayListGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'created_at')


class PlayListAdmin(admin.ModelAdmin):
    list_display = ('group', 'track', 'order', 'created_at')


admin.site.register(PlayListGroup, PlayListGroupAdmin)
admin.site.register(PlayList, PlayListAdmin)