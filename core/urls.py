from django.urls import path
from . import views
app_name = "core"

urlpatterns = [
    path('posts/', views.PostListView.as_view(), name='posts')
]