from django.db import models
from django.conf import settings

from tracks.models import Track

# 플레이리스트 그룹
class PlayListGroup(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='play_list')
    name = models.CharField('이름', max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = '플레이리스트 그룹'

    def __str__(self):
        return self.name


# 플레이리스트
class PlayList(models.Model):
    group = models.ForeignKey(PlayListGroup, verbose_name='그룹', on_delete=models.CASCADE, related_name='play_list')
    track = models.ForeignKey(Track, verbose_name='트랙', on_delete=models.CASCADE, related_name='play_list')
    order = models.IntegerField(verbose_name='플레이리스트 순서')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = '플레이리스트'
        ordering = ['order']