from .models import Post, PostLike, Comment
from .serializers import CommentSerializer

def serialize_posts(request, posts):
    serializePosts = []
    for post in posts:
        post_like = PostLike.objects.filter(post=post).count()
        post_comments = Comment.objects.filter(post=post)
        post_comments_list = [{
            "content":post.content,
            "timestamp":post.timestamp,
            "user":post.user.username
        } for post in post_comments]
        post_categories = [post.get('name') for post in post.categories.values()]
    
        postData = {
            "title":post.title,
            "content":post.content,
            "timestamp":post.timestamp,
            "image":post.image,
            "like":post_like,
            "comments":post_comments_list,
            "categories":post_categories
        }
        serializePosts.append(postData)
    yield serializePosts