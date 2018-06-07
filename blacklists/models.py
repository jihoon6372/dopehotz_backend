from django.db import models

class BlackList(models.Model):
    ip_addr = models.GenericIPAddressField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = '블랙리스트'
    
    def __str__(self):
        return self.ip_addr