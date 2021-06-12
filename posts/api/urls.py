from django.urls import path

from . import views

app_name = 'posts_api'

urlpatterns = [
    path('', views.following_post_list, name='list-following'),
    path('all/',  views.all_post_list, name='list-all'),
    path('create/', views.post_create, name='create'),
    path('vote/', views.post_vote, name='vote'),
    path('popular/', views.post_popular, name='popular'),
    path('<str:postId>/', views.post_detail, name='detail'),
    path('<str:postId>/delete/', views.post_delete, name='delete'),
]
