from django.contrib import admin

from .models import Notice, Report, ReportType

class NoticeAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at', 'updated_at')


class ReportAdmin(admin.ModelAdmin):
    list_display = ('user', 'content', 'report_type', 'created_at')


class ReportTypeAdmin(admin.ModelAdmin):
    list_display = ('name', )


admin.site.register(Notice, NoticeAdmin)
admin.site.register(Report, ReportAdmin)
admin.site.register(ReportType, ReportTypeAdmin)