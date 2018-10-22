from django.db import models
from django.conf import settings
from django.utils.text import slugify
from datetime import datetime

class Notice(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='article_notice')
    title = models.CharField('제목', max_length=100)
    slug = models.SlugField('SLUG', unique=True, max_length=100, allow_unicode=True, null=True, blank=True, help_text='자동 입력')
    content = models.TextField(blank=True, null=True, verbose_name='내용')
    is_delete = models.BooleanField(default=False, verbose_name='삭제 여부', help_text='게시물을 삭제하는 대신 이부분을 체크 하세요.')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        verbose_name_plural = '공지사항'
        ordering = ['-created_at']


    def __str__(self):
        return self.title

    
    def _get_unique_slug(self):
        dt = datetime.now().strftime("%Y%m%d%H%M%S")
        slug = slugify(self.title, allow_unicode=True)
        unique_slug = '{}-{}'.format(slug, dt)

        return unique_slug


    def save(self, *args, **kargs):
        if not self.id:
            self.slug = self._get_unique_slug()
            
        super(Notice, self).save(*args, **kargs)


# 유저, 내용 베이스
class ReportBase(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='작성자', on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_user")
    content = models.TextField(blank=True, null=True, verbose_name='내용')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


# 신고하기 모델
class Report(ReportBase):
    pass