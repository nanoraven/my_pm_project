from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, ListView
from django.views.generic.list import MultipleObjectMixin

from .models import Post

def post_topics(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'topics.html', {'post': post})

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
