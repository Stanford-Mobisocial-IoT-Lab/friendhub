from rest_framework import serializers
from bbs.models import Post


class BbsSerializer(serializers.Serializer):
    author = serializers.CharField()
    post = serializers.CharField()
    date = serializers.DateTimeField()

    def create(self, validated_data):
        return Post.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.author = validated_data.get('author', instance.author)
        instance.post = validated_data.get('post', instance.post)
        instance.date = validated_data.get('date', instance.date)
        instance.save()
        return instance


