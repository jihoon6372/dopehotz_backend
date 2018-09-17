from django.db import models

class DiscordLog(models.Model):
    log_message = models.TextField(blank=True, null=True, verbose_name='로그 내용')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.log_message)[:20]


class DiscordNotActiveDate(models.Model):
    not_day = models.IntegerField(verbose_name='비활성 날짜', unique=True)