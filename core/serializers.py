from rest_framework import serializers
#models
from .models import (Post, Category, Comment)

#post model serializer
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post 
        fields = (
            'id',
            'title',
            'content',
            'category',
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
            # 'user',
            # 'likes'
        )