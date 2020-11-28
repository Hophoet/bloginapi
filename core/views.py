from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
#rest framework
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from rest_framework.status import HTTP_404_NOT_FOUND
from rest_framework.response import Response
from rest_framework.views import APIView
#models
from .models import (Post, Comment)
#serializers
from .serializers import (PostSerializer, CommentSerializer)


class PostListView(APIView):
    def get(self, request, *args, **kwargs):
        posts = Post.objects.all()
        posts_serializer = PostSerializer(posts, many=True)
        return Response(posts_serializer.data)

class PostDetailView(APIView):
    def get(self, request, *args, **kwargs):
        post_id = kwargs.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        post_serializer = PostSerializer(post)
        return Response(post_serializer.data)

class PostCommentsView(APIView):
    def get(self, request, *args, **kwargs): 
        try:
            post_id = kwargs.get('post_id')
            post = Post.objects.get(pk=post_id)
            comments = Comment.objects.filter(post=post_id).order_by('-timestamp')
            post_serializer = PostSerializer(post)
            comments_serializer = CommentSerializer(comments, many=True)
        except Exception as error:
            return Response({'detail': f'{error}'}, status=HTTP_404_NOT_FOUND)
            # raise NotFound
        else:
            return Response(comments_serializer.data)