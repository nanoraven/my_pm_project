from django.contrib import admin
from django.contrib.auth.models import User
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.

class Post(models.Model):

    title = models.CharField(max_length=100,null=False)
    text = RichTextUploadingField(blank=True, default='')
    createad_in = models.DateTimeField(auto_now_add=True)
    createad_by = models.ForeignKey(User,related_name='users')
    is_published = models.BooleanField(default=False)

    def __unicode__(self):
        return self.title


class Comment(models.Model):

    post_id = models.ForeignKey(Post,related_name='posts')
    author = models.CharField(max_length=50)
    text = models.TextField(max_length=300)
    created_in = models.DateTimeField(auto_now_add=True)

