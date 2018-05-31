from django.db import models
from django.conf import settings
from django.utils.text import slugify

from tagging.fields import TagField

class Track(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='track')
    track_id = models.IntegerField(null=True, unique=True, verbose_name='트랙 ID')
    title = models.CharField('제목', max_length=100)
    slug = models.SlugField('SLUG', unique=True, max_length=100, allow_unicode=True, null=True, help_text='자동 입력')
    tape_info = models.TextField(blank=True, null=True, verbose_name='Tape INFO')
    lyrics = models.TextField(blank=True, null=True, verbose_name='lyrics')
    genre = models.CharField(max_length=255, blank=True, null=True, verbose_name='장르')
    image_url = models.CharField(max_length=255, blank=True, null=True, verbose_name='이미지 URL')
    download_url = models.CharField(max_length=255, blank=True, null=True, verbose_name='다운로드 URL')
    waveform_url = models.CharField(max_length=255, blank=True, null=True, verbose_name='Waveform URL')
    view_count = models.IntegerField(default=0, verbose_name='조회 수')
    likes = models.IntegerField(default=0, verbose_name='좋아요')
    track_score = models.IntegerField(default=0, verbose_name='트랙 점수')
    on_stage = models.IntegerField(default=0, db_index=True, verbose_name='온스테이지')
    tag = TagField()
    is_deleted = models.BooleanField(default=False, db_index=True, verbose_name='삭제여부', help_text='트랙을 삭제하는 대신 이부분을 체크 하세요.')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    duration = models.IntegerField(default=0, verbose_name='곡 길이')
    

    class Meta:
        verbose_name_plural = '트랙'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def _get_unique_slug(self):
        slug = slugify(self.title, allow_unicode=True)
        unique_slug = slug
        num = 1

        while Track.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1

        return unique_slug


    def save(self, *args, **kargs):
        if not self.id:
            self.slug = self._get_unique_slug()
            
        super(Track, self).save(*args, **kargs)


class TrackComment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="작성자", on_delete=models.CASCADE, related_name='track_comment')
    parent = models.ForeignKey("self", verbose_name="부모 댓글", on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    track = models.ForeignKey(Track, verbose_name="트랙", on_delete=models.CASCADE, related_name='comment')
    content = models.TextField(verbose_name='내용')
    is_deleted = models.BooleanField(default=False, db_index=True, verbose_name='삭제여부', help_text='댓글을 삭제하는 대신 이 부분을 체크하세요.')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = '댓글'
        ordering = ['created_at']
    
    def __str__(self):
        return self.content