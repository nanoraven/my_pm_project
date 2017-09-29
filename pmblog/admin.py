from django.contrib import admin

# Register your models here.

from .models import Post
admin.site.register(Post)

class PostAdmin(admin.ModelAdmin):
    fieldsets = ('title','createad_by')
