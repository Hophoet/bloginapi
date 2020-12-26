""" core add serializers modules """

from rest_framework import serializers
#models
from .models import (Post, Category, Comment, PostLike, CommentLike)


class PostSerializer(serializers.Serializer):
    """ post model serializer """
    id = serializers.IntegerField()
    title = serializers.CharField()
    content = serializers.CharField()
    categories = serializers.ListField()
    timestamp = serializers.DateTimeField()
    image = serializers.URLField()
    like = serializers.IntegerField()
    comments = serializers.ListField()

#category model serializer
class CategorySerializer(serializers.ModelSerializer):
    """ category model serializer """
    class Meta:
        """ category model serializer Meta class """
        model = Category
        fields = (
            'id',
            'name'
        )

#comment model serializer
class CommentSerializer(serializers.ModelSerializer):
    """ comment model serializer """
    class Meta:
        """ comment model serializer Meta class """
        model = Comment
        fields = (
            'content',
            'timestamp',
            'user',
            'post'
        )

class PostLikeSerializer(serializers.Serializer):
    """ post liking model serialier """
    post_id = serializers.IntegerField()
   

class CommentLikeSerializer(serializers.Serializer):
    """ comment like serializer """
    comment_id = serializers.IntegerField()

class PostEditSerializer(serializers.Serializer):
    """ post editing serializer """
    title = serializers.CharField(label=('Title'))
    content = serializers.CharField(
        label=('Content'),
        style={'input_type':'textarea'}
    )
    categories = serializers.IntegerField()
    image  = serializers.CharField(label=('Image'))
    post = serializers.IntegerField()


class PostDeleteSerializer(serializers.Serializer):
    """ post deleting serializer """
    post_id = serializers.IntegerField(label=('Post_id'))

class UserProfileSerializer(serializers.Serializer):
    """ user profile serializer """
    post = serializers.IntegerField()
    like = serializers.IntegerField()
    comment = serializers.IntegerField()
    name = serializers.CharField()
    