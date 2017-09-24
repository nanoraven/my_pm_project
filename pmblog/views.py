from django.http import Http404
from django.shortcuts import render, get_object_or_404
from .models import Post

def home(request):
    posts = Post.objects.all()
    return render(request, 'home.html', {'posts': posts})

def post_topics(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'topics.html', {'post': post})