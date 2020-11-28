from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
#rest framework
from rest_framework.permissions import IsAuthenticated
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