from django.db import models
from django.conf import settings


class News(models.Model):
    title = models.CharField(max_length=500)
    slug = models.SlugField(max_length=255, unique=True)
    text = models.TextField()
    image_path = models.CharField(max_length=255, blank=True, null=True)
    tickers = models.JSONField(default=list)
    source = models.CharField(max_length=255, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    def get_image_url(self):
        if self.image_path:
            return settings.MEDIA_URL + self.image_path
        else:
            return 