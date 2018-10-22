from django.contrib import admin

from .models import Notice, Report

class NoticeAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at', 'updated_at')


class ReportAdmin(admin.ModelAdmin):
    list_display = ('user', 'content', 'created_at')


admin.site.register(Notice, NoticeAdmin)
admin.site.register(Report, ReportAdmin)