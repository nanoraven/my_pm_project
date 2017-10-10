from django.contrib import admin
from django.contrib.auth.models import User
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.

class Post(models.Model):

    title = models.CharField(max_length=100,null=False)
    text = RichTextUploadingField(blank=True, default='')
    created_in = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=False)
    owner = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)


class Comment(models.Model):

    post_id = models.ForeignKey(Post,related_name='posts')
    author = models.CharField(max_length=50)
    text = models.TextField(max_length=300)
    created_in = models.DateTimeField(auto_now_add=True)

