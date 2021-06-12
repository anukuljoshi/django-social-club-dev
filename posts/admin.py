from django.contrib import admin

from .models import (
    Post, 
    Upvote, 
    Downvote
)

admin.site.register(Post)
admin.site.register(Upvote)
admin.site.register(Downvote)