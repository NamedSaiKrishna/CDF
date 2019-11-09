from django.conf.urls import url
from django.urls import path
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView,
    SearchPostListView, TrendListView)
from . import views

urlpatterns = [
    # path('', views.home, name='home'),
    path('feed/', PostListView.as_view(), name='feed'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('search/', SearchPostListView.as_view(), name='search-post'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('comment/<int:pk>/like/', views.like_comment, name='like_comment'),
    path('comment/<int:pk>/approve/', views.comment_approve, name='comment_approve'),
    path('comment/<int:pk>/remove/', views.comment_remove, name='comment_remove'),
    path('post/<int:pk>/comment/', views.add_comment_to_post, name='add_comment_to_post'),
    path('trending/', TrendListView.as_view(), name='trend'),
]
