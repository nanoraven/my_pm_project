"""my_pm_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from pmblog import views
from django.conf.urls.static import static
from my_pm_project import settings
from pmblog.views import HomePageView, PrivatePostList, PostTopicDetailView, PrivatePostTopicDetailView, ContentListView

urlpatterns = [
    url(r'^$', HomePageView.as_view(), name='home'),
    url(r'^posts/$', HomePageView.as_view(), name='home_2'),
    url(r'^contents/$', ContentListView.as_view(), name='content_list'),
    # url(r'^posts/(?P<pk>\d+)/$', views.post_topics, name='post_topics'),
    url(r'^posts/(?P<pk>\d+)/$', PostTopicDetailView.as_view(), name='post_topics'),
    url(r'^posts_private/$', PrivatePostList.as_view(), name='private_posts'),
    url(r'^posts_private/(?P<pk>\d+)/$', PrivatePostTopicDetailView.as_view(), name='private_post_detail'),
    url(r'^admin/', admin.site.urls),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^posts_private/page/(?P<page>\d+)/$', PrivatePostList.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
