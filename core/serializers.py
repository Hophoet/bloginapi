from rest_framework import serializers
#models
from .models import (Post, Category, Comment, PostLike, CommentLike)

#post model serializer
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post 
        fields = (
            'id',
            'title',
            'content',
            'categories',
            'timestamp',
            'image',
            # 'likes',
            # 'comments'
        
        )

#comment model serializer
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = (
            'content',
            'timestamp',
            'user',
            'post'
        )

class PostLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostLike
        fields = (
            'user',
            'post'
        )

class CommentLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentLike
        fields = (
            'user',
            'comment'
        )

class PostEditSerializer(serializers.Serializer):
    title = serializers.CharField(label=('Title'))
    content = serializers.CharField(
        label=('Content'),
        style={'input_type':'textarea'}
    )
    categories = serializers.IntegerField()
    image  = serializers.CharField(label=('Image'))
    post = serializers.IntegerField()