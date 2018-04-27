from rest_framework import serializers
from bbs.models import Post


class BbsSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Post
        fields = ('author', 'post', 'date')


