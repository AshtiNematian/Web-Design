from rest_framework import serializers
from .models import Post


class PostSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        post = Post.objects.create(**validated_data)

        return post

    class Meta:
        model = Post
        fields = [
            'title',
            'description',
            'category',
            'author',
            'published'
        ]
