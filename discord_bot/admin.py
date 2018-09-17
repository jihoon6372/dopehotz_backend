from django.contrib import admin

from .models import *

class DiscordLogAdmin(admin.ModelAdmin):
    list_display = ('log_message', 'created_at')
    readonly_fields = ('created_at',)

admin.site.register(DiscordLog, DiscordLogAdmin)