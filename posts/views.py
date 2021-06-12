from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def post_list(request, *args, **kwargs):
    return render(request, 'posts/list.html', {})


# unauthorized
def error_401_view(request, *args, **kwargs):
    return render(request, '401.html', {})


# not found
def error_404_view(request, *args, **kwargs):
    return render(request, '404.html', {})


# not allowed
def error_405_view(request, *args, **kwargs):
    return render(request, '405.html', {})