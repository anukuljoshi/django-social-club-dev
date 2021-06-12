from django.urls import path

from . import views

app_name = 'users_api'

urlpatterns = [
    path('self/', views.request_user_detail , name='self-detail'),
    path('follow/', views.user_add_remove_follow , name='follow'),
    path('edit/', views.user_update , name='edit'),
    path('<int:userId>/', views.user_detail , name='detail'),
    path('<int:userId>/posts/', views.user_post_list , name='posts'),
    path('<int:userId>/upvoted/posts/', views.user_liked_post_list , name='upvoted-posts'),
    path('<int:userId>/followers/', views.user_followers, name='followers'),
    path('<int:userId>/following/', views.user_following, name='following'),
]
