from django.db import models
from django.shortcuts import redirect
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


def get_absolute_url():
    return reverse('feed', )


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def approved_comments(self):
        return self.comments.filter(approved_comment=True)

    def get_absolute_url(self):
        pass


class Comment(models.Model):
    post = models.ForeignKey('forum.Post', on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)
    likes = models.ManyToManyField(User, related_name='likes', blank=True)

    def total_likes(self):
        return self.likes.count()

    class Meta:
        ordering = ('-created_date',)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text

    def get_absolute_url(self):
        pass
