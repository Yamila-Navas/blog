from django.urls import path
from . import views
from .feeds import LatestPostsFeed

app_name = 'blog'

urlpatterns = [
    # /blog/
    # path('', views.PostListView.as_view(), name='post_list'),

    # /blog/
    path('', views.post_list, name='post_list'),

    # /blog/tags/some-tag/
    path('tags/<slug:tag_slug>/', views.post_list, name='post_list_by_tag'),

    #/blog/2024/06/15/sample-post/
    path('<int:year>/<int:month>/<int:day>/<slug:slug>/', views.post_detail, name='post_detail'),

    # /blog/1/share/
    path('<int:post_id>/share/', views.post_share, name='post_share'),

    # /blog/1/comment/
    path('<int:post_id>/comment/', views.post_comment, name='post_comment'),

    # /blog/feed/
    path('feed/', LatestPostsFeed(), name='post_feed'),

    # /blog/search/
    path('search/', views.post_search, name='post_search'),

    ]