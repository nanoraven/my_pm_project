from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.list import MultipleObjectMixin

from .models import Post

import logging
logger = logging.getLogger(__name__)

class PostTopicDetailView(DetailView, SingleObjectMixin):
    template_name = "topics.html"
    queryset = Post.objects.filter(is_published=True)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Post.objects.filter(is_published=True))
        return super(PostTopicDetailView,self).get(request,*args,**kwargs)

    def get_context_data(self, **kwargs):
        context = super(PostTopicDetailView,self).get_context_data(**kwargs)

        pk=int(self.kwargs['pk'])
        post_prev = Post.objects.filter(pk=str(pk-1))
        post_next = Post.objects.filter(pk=str(pk+1))

        context["post"] = self.object
        if (not post_next) or post_next==1:
            context["post_next"] = -1
        else:
            if post_next[0].is_published:
                context["post_next"] = post_next[0]
                logger.error("Is published? - {}", post_next[0].is_published)
            else:
                context["post_next"] = -1

        if (not post_prev) or post_prev== -1:
            context["post_prev"] = -1
        else:
            if post_prev[0].is_published:
                context["post_prev"] = post_prev[0]
            else:
                context["post_prev"] = -1
        logger.error("pk = {}".format(pk))
        logger.error("Post prev = {}".format(post_prev))
        logger.error("Post next = {}".format(post_next))
        return context

class PrivatePostTopicDetailView(DetailView, SingleObjectMixin):
    model = Post
    template_name = "private_post_detail.html"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(PrivatePostTopicDetailView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Post.objects.all())
        return super(PrivatePostTopicDetailView,self).get(request,*args,**kwargs)

    def get_context_data(self, **kwargs):
        context = super(PrivatePostTopicDetailView,self).get_context_data(**kwargs)

        pk=int(self.kwargs['pk'])
        post_prev = Post.objects.filter(pk=str(pk-1))
        post_next = Post.objects.filter(pk=str(pk+1))

        context["post"] = self.object
        if (not post_next) or post_next==1:
            context["post_next"] = -1
        else:
            context["post_next"] = post_next[0]

        if (not post_prev) or post_prev== -1:
            context["post_prev"] = -1
        else:
            context["post_prev"] = post_prev[0]

        logger.error("pk = {}".format(pk))
        logger.error("Post prev = {}".format(post_prev))
        logger.error("Post next = {}".format(post_next))
        return context

class HomePageView(TemplateView):
    template_name = "home.html"
    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        return context

    def get(self, request, *args, **kwargs):
        posts_list = Post.objects.filter(is_published=True)
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
        context = self.get_context_data()
        context['all_articles'] = Post.objects.filter(is_published=True).order_by('createad_in')
        context['posts'] = posts_list
        return self.render_to_response(context)

class PrivatePostList(ListView,MultipleObjectMixin):
    model = Post
    paginate_by = 2
    context_object_name = 'posts'
    template_name = 'private_posts.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        """
        Декорируем диспетчер функцией login_required, чтобы запретить просмотр отображения неавторизованными
        пользователями
        """
        return super(PrivatePostList, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Post.objects.all()

class ContentList(ListView,MultipleObjectMixin):
    model = Post
    context_object_name = 'contents'
    template_name = 'contents.html'