from django.urls import path
from . import views
app_name = "core"

urlpatterns = [
    path('posts/', views.PostListView.as_view(), name='posts'),
    path('post/<int:post_id>/', views.PostDetailView.as_view(), name='post_detail'),
    path('post/<int:post_id>/comments/', views.PostCommentsView.as_view(), name='post_comments'),
]