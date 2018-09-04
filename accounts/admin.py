from django.contrib import admin
from .models import Profile, SoundcloudInfo

class ProfileAdmin(admin.ModelAdmin):
    model = Profile
    list_display = ('user', 'name', 'soundcloud_id')

    def name(self, obj):
        return obj.user.last_name+obj.user.first_name
    name.short_description = '이름'


class SoundcloudInfoAdmin(admin.ModelAdmin):
    model = SoundcloudInfo
    list_display = ('user', 'token')



admin.site.register(Profile, ProfileAdmin)
admin.site.register(SoundcloudInfo, SoundcloudInfoAdmin)