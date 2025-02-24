from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


class Post(models.Model):

    class Status(models.TextChoices):
        PUBLISHED="PB","Published"
        DRAFT="DF","Draft"
    title=models.CharField(max_length=250)
    slug=models.SlugField(max_length=250)
    body=models.TextField()
    author=models.ForeignKey(User,on_delete=models.CASCADE,related_name='blog_posts')
    publish=models.DateTimeField(default=timezone.now)
    create=models.DateTimeField(auto_now_add=True)
    update=models.DateTimeField(auto_now=True)
    status=models.CharField(max_length=2,choices=Status.choices,default=Status.DRAFT)

    objects=models.Manager()
    published=PublishedManager()

    class Meta:
        ordering=['-publish']
        indexes=[
            models.Index(fields=['-publish']),
        ]


    def __str__(self):
        return self.title