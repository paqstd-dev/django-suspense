import time
from random import randrange

from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    content = models.TextField(blank=True)

    @property
    def read_time(self):
        return randrange(10)


class SlowPost(Post):
    @property
    def read_time(self):
        time.sleep(1)
        return randrange(10)

    class Meta:
        proxy = True
