from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from .models import Post

def home(request):
    posts_list = Post.objects.all()
    paginator = Paginator(posts_list, 2)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        posts = paginator.page(paginator.num_pages)
    return render(request, 'home.html', {'posts': posts})

def post_topics(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'topics.html', {'post': post})