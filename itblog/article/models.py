from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
     

class Article(models.Model):
    title = models.CharField(max_length=255) #в django по умолчанию nullable=False (null=True, blank=True нужно прописывать если нужно)
    text = models.TextField()
    likes = models.IntegerField(default=0)
    active = models.BooleanField(default=True)
    author = models.ForeignKey(to='Author', on_delete=models.CASCADE,  #ForeignKey вместо OneToMany
        related_name="articles", null=True, blank=True) 

    readers = models.ManyToManyField(to=User, 
        related_name="articles",
        blank=True)
    
    published = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    picture = models.ImageField(null=True, blank=True, 
        upload_to="articles/" + datetime.today().strftime("%Y%m%d"))  
    dislikes = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    reposts = models.IntegerField(default=0)
    tag = models.ManyToManyField("Tag", blank=True, related_name="article")

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "статью"
        verbose_name_plural = "Статьи"



class Author(models.Model):
    name = models.CharField(max_length=255)
    photo = models.ImageField(upload_to="author_photo", null=True, blank=True)
    user = models.OneToOneField(to=User, 
        on_delete=models.SET_NULL, 
        related_name="author", null=True, blank=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "автора"
        verbose_name_plural = "Авторы"

# on delete - при удалении автора что происходит со статьями

class Comment(models.Model):
    article = models.ForeignKey(to=Article, 
        on_delete=models.CASCADE,
        related_name="comments")
    text = models.TextField()
    user = models.ForeignKey(to=User, 
        on_delete=models.CASCADE, 
        related_name="comments")
    
    def __str__(self):
        return self.user.username + " - " + self.text #можно через перевод в str

    class Meta:
        verbose_name = "комментарий"
        verbose_name_plural = "Комметарии"
        ordering = ["-user"]

class Tag(models.Model):
    name = models.CharField(max_length=55)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "тэг"
        verbose_name_plural = "Тэги"