from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from . import views

# urlpatterns = [
#     url(r'^users',),
#     url(r'^posts',),
# ]

router = DefaultRouter()
router.register(r'posts', views.PostViewSet)
router.register(r'users', views.UserViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]