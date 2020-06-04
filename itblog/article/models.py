from django.db import models

class Article(models.Model):
    title = models.CharField(max_length=255) #в django по умолчанию nullable=False (null=True, blank=True нужно прописывать если нужно)
    text = models.TextField()
    likes = models.IntegerField(default=0)
    active = models.BooleanField(default=True)
    