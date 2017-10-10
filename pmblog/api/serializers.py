from django.contrib.auth.models import User
from rest_framework import serializers

from ..models import Post


class PostSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    owner_url = serializers.HyperlinkedRelatedField(view_name='user-detail', source='owner.id', queryset=User.objects.all())

    class Meta:
        model = Post
        fields = ('url', 'id', 'title', 'text', 'created_in','is_published', 'owner', 'owner_url')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    posts = serializers.HyperlinkedRelatedField(many=True, view_name='post-detail', read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'username', 'posts')