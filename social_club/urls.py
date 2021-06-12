from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from posts.views import error_401_view, error_404_view, error_405_view, post_list

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', post_list, name='home'),
    path('posts/', include('posts.urls')),
    path('users/', include('users.urls')),
    path('api/posts/', include('posts.api.urls')),
    path('api/auth/', include('users.api.urls')),
    path('error/401/', error_401_view, name='error401'),
    path('error/404/', error_404_view, name='error404'),
    path('error/405/', error_405_view, name='error405'),
]
