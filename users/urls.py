from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('<int:userId>/', views.user_profile_view, name='profile'),
    path('<int:userId>/edit/', views.user_edit_view, name='edit'),
]
