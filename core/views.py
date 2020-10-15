""" core app views module """

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
#rest framework
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.status import HTTP_404_NOT_FOUND
from rest_framework.response import Response
from rest_framework.views import APIView
#models
from .models import (Post, Comment, PostLike, CommentLike, 
Category)
#serializers
from .serializers import (PostSerializer, CommentSerializer, 
    PostLikeSerializer, CommentLikeSerializer, PostEditSerializer,
    CategorySerializer, PostDeleteSerializer, UserProfileSerializer)


class PostListView(APIView):
    """ posts listing view """
    def get(self, request, *args, **kwargs):
        """ get request method """
        posts = Post.objects.all()
        posts_serializer = PostSerializer(posts, many=True)
        return Response(posts_serializer.data)


class CategoryListView(APIView):
    """ categories listing view """
    def get(self, request, *args, **kwargs):
        """ post request method """
        categories = Category.objects.all()
        categories_serializer = CategorySerializer(categories, many=True)
        return Response(categories_serializer.data)


class PostDetailView(APIView):
    """ post detail view """
    def get(self, request, *args, **kwargs):
        """ get request method """
        post_id = kwargs.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        post_serializer = PostSerializer(post)
        return Response(post_serializer.data)


class PostCommentsView(APIView):
    """ post comments listing view """
    def get(self, request, *args, **kwargs): 
        """ get request method """
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
    """ add new post view """
    permission_classes = (IsAuthenticated,)
    serializer_class = PostSerializer
    def post(self, request, *args, **kwargs):
        """ post request method """
        serializer = self.serializer_class(data=request.data,
                                            context={'request':request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        # raise NotFound


class AddCommentToPostView(APIView):
    """ add comment to post view """
    permission_classes = (IsAuthenticated,)
    serializer_class = CommentSerializer
    def post(self, request, *args, **kwargs):
        """ post request method """
        post_id = request.data.get('post_id')
        post = get_object_or_404(Post, pk=post_id)
        user = request.user
        content = request.data.get('content')
        data = {
            'content':content,
            'user':user.pk,
            'post':post.pk
        }
        comment_serializer = self.serializer_class(data=data,
                                                    context={'request':request}
                                                    )
        comment_serializer.is_valid(raise_exception=True)
        
      
        comment = comment_serializer.save()
        post.comment_set.set((comment,))
        return Response(comment_serializer.data)


class TogglePostLikeView(APIView):
    """ post like toggle view """
    permission_classes = (IsAuthenticated,)
    serializer_class = PostLikeSerializer
    def post(self, request, *args, **kwargs):
        """ post request method """
        post_like_serializer = self.serializer_class(data=request.data, context={'request':request})
        post_like_serializer.is_valid(raise_exception=True)
        post_id = request.data.get('post_id')
        post = get_object_or_404(Post, pk=post_id)
        user = request.user
        post_likes = PostLike.objects.filter(user=user, post=post)
        if post_likes.exists():
            # print('liked')
            post_like = post_likes.first()
            post_like.delete()
            return Response(
                {
                    'state': 'post disliked',
                    'likes': post_likes.count(),
                    'user': request.user.username
                }
                , status=200)

        PostLike.objects.create(user=user, post=post)
        return Response(
            {
                'state': 'post liked',
                'likes': post_likes.count(),
                'user': request.user.username
            }
            , status=200)
        

class ToggleCommentLikeView(APIView):
    """ comment like toggling view """
    permission_classes = (IsAuthenticated,)
    serializer_class = CommentLikeSerializer
    def post(self, request, *args, **kwargs):
        """ post request method """
        user = request.user
        comment_id = request.data.get('comment_id')
        comment = get_object_or_404(Comment, pk=comment_id)
        comment_like_serializer = self.serializer_class(data=request.data, context={'request':request})
        comment_like_serializer.is_valid(raise_exception=True)
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

        # comment_like_serializer.save()
        CommentLike.objects.create(user=user, comment=comment)
        return Response(
            {
                'state': 'comment liked',
                'likes': comment_likes.count(),
                'user': request.user.username
            }
            , status=200)

        raise NotFound

class PostIsLikedByUser(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request, *args, **kwargs):
        """ post request method """
        post_id = request.data.get('post_id')
        if not post_id:
            return Response(status=404, data={'detail':'post id not provided!'})
        post = get_object_or_404(Post, pk=post_id)
        user = request.user 
        post_like = PostLike.objects.filter(user=user, post=post)
        if(post_like):
            return Response(data={'post_is_liked':True},status=200)
        return Response(data={'post_is_liked':False},status=200)


        

class PostEditView(APIView):
    """ post editing view """
    permission_classes = (IsAuthenticated,)
    serializer_class = PostEditSerializer
    def post(self, request, *args, **kwargs):
        """ post request method """
        post_edit_serializer = self.serializer_class(data=request.data, context={'request':request})
        post_edit_serializer.is_valid(raise_exception=True)
        #get validated data
        validated_data = post_edit_serializer.validated_data
        post_id = validated_data.get('post')
        post = get_object_or_404(Post, pk=post_id)
        #check the authentificated user is the owner of the post
        if not request.user == post.author:
            raise PermissionDenied
 
        title = validated_data.get('title')
        content = validated_data.get('content')
        category_id = validated_data.get('categories')
        image = validated_data.get('image')
        
        #get objects
        category = get_object_or_404(Category, pk=category_id)
        #edit post
        post.title = title 
        post.content = content 
        post.image = image
        post.categories.clear()
        post.categories.set((category,))
        post.save()
        #serializer
        post_serializer = PostSerializer(post)
        return Response(post_serializer.data)

class PostDeleteView(APIView):
    """ post deleting view """
    permission_classes = (IsAuthenticated,)
    serializer_class = PostDeleteSerializer
    def post(self, request, *args, **kwargs):
        """ post request method """
        post_delete_serializer = self.serializer_class(data=request.data, context={'request':request})
        post_delete_serializer.is_valid(raise_exception=True)
        #get validated data
        validated_data = post_delete_serializer.validated_data
        post_id = validated_data.get('post_id')
        post = get_object_or_404(Post, pk=post_id)
        #check authorization
        if not post.author == request.user:
            raise PermissionDenied
        #delete post
        post.delete()
        return Response({'detail':('Post has been removed.')})

class UserProfile(APIView):
    """ user profile getter """
    permission_classes = (IsAuthenticated, )
    
    def get(self, request, *args, **kwargs):
        """ get request method """
        name = request.user.username
        post_count = Post.objects.filter(author=request.user).count()
        like_count = PostLike.objects.filter(post__author=request.user).count()
        comment_count = Comment.objects.filter(post__author=request.user).count()
        user_profile_serializer_data = {
            "name":name,
            "post":post_count,
            "like":like_count,
            "comment":comment_count
        }
        user_profile_serializer = UserProfileSerializer(data=user_profile_serializer_data, context={'request':request})
        user_profile_serializer.is_valid(raise_exception=True)
        return Response(user_profile_serializer.data)
    