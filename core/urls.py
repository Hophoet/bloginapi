from django.urls import path
from . import views
app_name = "core"

urlpatterns = [
    path('posts/', views.PostListView.as_view(), name='posts'),
    path('post/<int:post_id>/', views.PostDetailView.as_view(), name='post_detail'),
    path('post/<int:post_id>/comments/', views.PostCommentsView.as_view(), name='post_comments'),
    path('add-new-post/', views.AddNewPostView.as_view(), name='add_new_post'),
    path('post/<int:post_id>/add-comment/', views.AddCommentToPostView.as_view(), name='add_comment_to_post'),
    path('toggle-post-like/', views.TogglePostLikeView.as_view(), name='toggle_post_like'),
    path('toggle-comment-like/', views.ToggleCommentLikeView.as_view(), name='toggle_comment_like'),
]