from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
#rest framework
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from rest_framework.status import HTTP_404_NOT_FOUND
from rest_framework.response import Response
from rest_framework.views import APIView
#models
from .models import (Post, Comment, PostLike, CommentLike, 
Category)


#serializers
from .serializers import (PostSerializer, CommentSerializer, 
    PostLikeSerializer, CommentLikeSerializer, PostEditSerializer)


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


class AddNewPostView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PostSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                            context={'request':request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        # raise NotFound


class AddCommentToPostView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CommentSerializer
    def post(self, request, *args, **kwargs):
        post_id = kwargs.get('post_id')
        post = get_object_or_404(Post, pk=post_id)
        user = request.user
        content = request.data.get('content')
        data = {
            'content':content,
            'user':user.pk,
            'post':post.pk
        }
        comment_serializer = self.serializer_class(data=data,
                                                    context={'request':request})
        if comment_serializer.is_valid(raise_exception=True):
            
            comment = comment_serializer.save()
            print('COMMENT', comment)
            # print(post.comment_set.set)
            # print(request.data)
            post.comment_set.set((comment,))
            return Response(comment_serializer.data)

class TogglePostLikeView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PostLikeSerializer
    def post(self, request, *args, **kwargs):
        user = request.data.get('user')
        post = request.data.get('post')
        post_like_serializer = self.serializer_class(data=request.data, context={'request':request})
        if post_like_serializer.is_valid(raise_exception=True):
            post_likes = PostLike.objects.filter(user=user, post=post)
            # print(dir(post_likes), post_likes.count())
            if post_likes.exists():
                print('liked')
                post_like = post_likes.first()
                post_like.delete()
                return Response(
                    {
                        'state': 'post disliked',
                        'likes': post_likes.count(),
                        'user': request.user.username
                    }
                    , status=200)

            post_like_serializer.save()
            return Response(
                {
                    'state': 'post liked',
                    'likes': post_likes.count(),
                    'user': request.user.username
                }
                , status=200)
        



class ToggleCommentLikeView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CommentLikeSerializer
    def post(self, request, *args, **kwargs):
        user = request.data.get('user')
        comment = request.data.get('comment')
        comment_like_serializer = self.serializer_class(data=request.data, context={'request':request})
        if comment_like_serializer.is_valid(raise_exception=True):
            comment_likes = CommentLike.objects.filter(user=user, comment=comment)
            if comment_likes.exists():
                # print('liked')
                comment_like = comment_likes.first()
                comment_like.delete()
                return Response(
                    {
                        'state': 'comment disliked',
                        'likes': comment_likes.count(),
                        'user': request.user.username
                    }
                    , status=200)

            comment_like_serializer.save()
            return Response(
                {
                    'state': 'comment liked',
                    'likes': comment_likes.count(),
                    'user': request.user.username
                }
                , status=200)
        

class PostEditView(APIView):
    """ post edit view """
    permission_classes = (IsAuthenticated,)
    serializer_class = PostEditSerializer
    def post(self, request, *args, **kwargs):
        post_edit_serializer = self.serializer_class(data=request.data, context={'request':request})
        post_edit_serializer.is_valid(raise_exception=True)
        #get validated data
        validated_data = post_edit_serializer.validated_data
        title = validated_data.get('title')
        content = validated_data.get('content')
        category_id = validated_data.get('category')
        image = validated_data.get('image')
        post_id = validated_data.get('post')
        #get objects
        category = get_object_or_404(Category, pk=category_id)
        #edit post
        post = get_object_or_404(Post, pk=post_id)
        post.title = title 
        post.content = content 
        post.image = image
        post.category.clear()
        post.category.set((category,))
        post.save()
        #serializer
        post_serializer = PostSerializer(post)

        return Response(post_serializer.data)
