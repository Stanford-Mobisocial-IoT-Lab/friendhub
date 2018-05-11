from rest_framework import serializers
from sticky_notes.models import Post


class StickyNotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('author', 'post', 'date')


