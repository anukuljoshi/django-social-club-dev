from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages


User = get_user_model()


def signup_view(request, *args, **kwargs):
    if(request.user.is_authenticated):
        return redirect('home')
    if(request.POST):
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        if(len(username)<2 or len(username)>20):
            messages.error(request, 'Username must be between 2 and 20 characters.')
            return redirect('users:signup')
        # add error messages for email and password
        user = User.objects.create_user(username, email, password)
        if(user):
            messages.success(request, 'User created successfully.')
            return redirect('users:login')
        else:
            messages.errorr(request, 'Something went wrong. Try Again.')
            return redirect('users:signup')
    else:
        return render(request, 'users/signup.html', {})


def login_view(request, *args, **kwargs):
    if(request.user.is_authenticated):
        return redirect('home')
    if(request.POST):
        username = request.POST.get('username')
        password = request.POST.get('password')
        # next_path = request.POST.get('next')
        user = authenticate(request, username=username, password=password)
        if(user):
            login(request, user)
            # if(next_path=='None'):
            #     print('None')
            #     return redirect('posts:list')
            return redirect('home')
        else:
            messages.error(request, 'Username or password incorrect.')
            return redirect('users:login')
    else:
        # next_path = request.GET.get('next')
        # context = {
        #     "next_path": next_path
        # }
        return render(request, 'users/login.html', context={})


@login_required
def logout_view(request, *args, **kwargs):
    logout(request)
    return redirect('users:login')


@login_required
def user_profile_view(request, *args, **kwargs):
    userId = kwargs.get('userId')
    user = User.objects.filter(id=userId).first()
    if(user):
        context = {
            'username': user.username,
            'userId': user.id
        }
        return render(request, 'users/profile.html', context)
    return redirect('error404')


@login_required
def user_edit_view(request, *args, **kwargs):
    userId = kwargs.get('userId')
    user = User.objects.filter(id=userId).first()
    if(user==request.user):
        return render(request, 'users/edit.html', {})
    return redirect('users:edit', userId=request.user.id)