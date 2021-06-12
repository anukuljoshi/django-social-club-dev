from posts.api.views import POST_PER_PAGE
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from posts.models import Post, Upvote
from posts.api.serializers import PostSerializer

from ..models import Follow
from .serializers import UserProfileSerializer, UserUpdateSerializer

User = get_user_model()

POST_PER_PAGE = 2
USER_PER_PAGE = 2


@api_view(['GET'])
def request_user_detail(request, *args, **kwargs):
    errors = []
    if(request.user.is_authenticated):
        user_serializer = UserProfileSerializer(request.user, context={'request': request})
        return Response(user_serializer.data, status=status.HTTP_200_OK)
    else:
        errors.append('User not authenticated')
        return Response({"detail": "Not Authenticated", "errors": errors}, status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def user_add_remove_follow(request, *args, **kwargs):
    errors = []
    if(request.user.is_authenticated):
        userId = request.data.get('userId')
        following_user = User.objects.filter(id=userId).first()
        if(not following_user):
            errors.append('User not found.')
            return Response({'detail': 'not found error', 'errors': errors}, status=status.HTTP_404_NOT_FOUND)
        follower_user = request.user
        if(follower_user==following_user):
            return Response({'detail': 'Not allowed'})
        follow, created = Follow.objects.get_or_create(user_id=follower_user, following_user_id=following_user)
        if(created):
            return Response({'detail': 'Following'}, status=status.HTTP_200_OK)
        follow.delete()
        return Response({'detail': 'Unfollowed'}, status=status.HTTP_200_OK)
    else:
        errors.append('User not authenticated')
        return Response({"detail": "Not Authenticated", "errors": errors}, status.HTTP_401_UNAUTHORIZED)



@api_view(['POST'])
def user_update(request, *args, **kwargs):
    errors = []
    if(request.user.is_authenticated):
        username = request.data.get('username')
        email = request.data.get('email')
        display_name = request.data.get('display_name')
        bio = request.data.get('bio')
        if(len(username)<2 or len(username)>20):
            errors.append('Username must be between 2 and 20 characters.')
        if(len(display_name)<2 or len(display_name)>40):
            errors.append('Display name must be between 2 and 40 characters.')
        if(len(bio)>128):
            errors.append('Bio must be less than 128 characters.')
        if(len(errors)>0):
            return Response({'detail': 'validation error', 'errors': errors}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.filter(pk=request.user.id).first()
        if(not user):
            errors.append('User not found.')
            return Response({'detail': 'not found error', 'errors': errors}, status=status.HTTP_404_NOT_FOUND)
        username_user = User.objects.filter(username=username).first()
        email_user = User.objects.filter(email=email).first()
        if(username_user and user.id!=username_user.id):
            errors.append('Username not available.')
        if(email_user and user.id!=email_user.id):
            errors.append('Email already in use.')
        if(len(errors)>0):
            return Response({'detail': 'Validation error', 'errors': errors}, status=status.HTTP_200_OK)
        else:
            profile = user.profile
            user.username = username
            user.email = email
            profile.display_name = display_name
            profile.bio = bio
            user.save()
            profile.save()
            user_serializer = UserUpdateSerializer(user, context={'request': request})
            return Response(user_serializer.data, status=status.HTTP_201_CREATED)
    else:
        errors.append('User not authenticated')
        return Response({"detail": "Not Authenticated", "errors": errors}, status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
def user_detail(request, *args, **kwargs):
    errors = []
    if(request.user.is_authenticated):
        userId = kwargs.get('userId')
        user = User.objects.filter(id=userId).first()
        if(not user):
            errors.append('User not found.')
            return Response({'detail': 'not found error', 'errors': errors}, status=status.HTTP_404_NOT_FOUND)
        user_serializer = UserProfileSerializer(user, context={'request': request})
        return Response(user_serializer.data, status=status.HTTP_200_OK)
    else:
        errors.append('User not authenticated')
        return Response({"detail": "Not Authenticated", "errors": errors}, status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
def user_post_list(request, *args, **kwargs):
    errors = []
    if(request.user.is_authenticated):
        userId = kwargs.get('userId')
        user = User.objects.filter(id=userId).first()
        if(not user):
            errors.append('User not found.')
            return Response({'detail': 'not found error', 'errors': errors}, status=status.HTTP_404_NOT_FOUND)
        page_number = int(request.query_params.get('page', 1))
        OFFSET = POST_PER_PAGE*(page_number-1)
        LIMIT = POST_PER_PAGE
        TOTAL = Post.objects.filter(user=user).count()
        has_next_page = False
        has_prev_page = False
        if(OFFSET+LIMIT<TOTAL):
            has_next_page = True
        if(OFFSET+LIMIT>POST_PER_PAGE):
            has_prev_page = True
        posts = Post.objects.filter(user=user)[OFFSET: OFFSET+LIMIT]
        posts_serializer = PostSerializer(posts, many=True, context={'request': request})
        return Response({
            'posts': posts_serializer.data, 
            'has_next_page': has_next_page,
            'has_prev_page': has_prev_page
        }, status.HTTP_200_OK)
    else:
        errors.append('User not authenticated')
        return Response({"detail": "Not Authenticated", "errors": errors}, status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
def user_liked_post_list(request, *args, **kwargs):
    errors = []
    if(request.user.is_authenticated):
        userId = kwargs.get('userId')
        user = User.objects.filter(id=userId).first()
        if(not user):
            errors.append('User not found.')
            return Response({'detail': 'not found error', 'errors': errors}, status=status.HTTP_404_NOT_FOUND)
        page_number = int(request.query_params.get('page', 1))
        OFFSET = POST_PER_PAGE*(page_number-1)
        LIMIT = POST_PER_PAGE
        liked_posts = Upvote.objects.filter(user=user).values_list('post', flat=True).all()
        TOTAL = Post.objects.filter(id__in=liked_posts).count()
        has_next_page = False
        has_prev_page = False
        if(OFFSET+LIMIT<TOTAL):
            has_next_page = True
        if(OFFSET+LIMIT>POST_PER_PAGE):
            has_prev_page = True
        posts = Post.objects.filter(id__in=liked_posts)[OFFSET: OFFSET+LIMIT]
        posts_serializer = PostSerializer(posts, many=True, context={'request': request})
        return Response({
            'posts': posts_serializer.data, 
            'has_next_page': has_next_page,
            'has_prev_page': has_prev_page
        }, status.HTTP_200_OK)
    else:
        errors.append('User not authenticated')
        return Response({"detail": "Not Authenticated", "errors": errors}, status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
def user_followers(request, *args, **kwargs):
    errors = []
    if(request.user.is_authenticated):
        userId = kwargs.get('userId')
        user = User.objects.filter(id=userId).first()
        if(not user):
            errors.append('User not found.')
            return Response({'detail': 'not found error', 'errors': errors}, status=status.HTTP_404_NOT_FOUND)
        page_number = int(request.query_params.get('page', 1))
        OFFSET = USER_PER_PAGE*(page_number-1)
        LIMIT = USER_PER_PAGE
        followers = Follow.objects.filter(following_user_id=user).values_list('user_id', flat=True).all()
        TOTAL = User.objects.filter(id__in=followers).count()
        has_next_page = False
        has_prev_page = False
        if(OFFSET+LIMIT<TOTAL):
            has_next_page = True
        if(OFFSET+LIMIT>USER_PER_PAGE):
            has_prev_page = True

        users = User.objects.filter(id__in=followers)[OFFSET: OFFSET+LIMIT]
        users_serializer = UserProfileSerializer(users, many=True, context={'request': request})
        return Response({
            'users': users_serializer.data, 
            'has_next_page': has_next_page,
            'has_prev_page': has_prev_page
        }, status.HTTP_200_OK)
    else:
        errors.append('User not authenticated')
        return Response({"detail": "Not Authenticated", "errors": errors}, status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
def user_following(request, *args, **kwargs):
    errors = []
    if(request.user.is_authenticated):
        userId = kwargs.get('userId')
        user = User.objects.filter(id=userId).first()
        if(not user):
            errors.append('User not found.')
            return Response({'detail': 'not found error', 'errors': errors}, status=status.HTTP_404_NOT_FOUND)
        page_number = int(request.query_params.get('page', 1))
        OFFSET = USER_PER_PAGE*(page_number-1)
        LIMIT = USER_PER_PAGE
        following = Follow.objects.filter(user_id=user).values_list('following_user_id', flat=True).all()
        TOTAL = User.objects.filter(id__in=following).count()
        has_next_page = False
        has_prev_page = False
        if(OFFSET+LIMIT<TOTAL):
            has_next_page = True
        if(OFFSET+LIMIT>USER_PER_PAGE):
            has_prev_page = True
        users = User.objects.filter(id__in=following)[OFFSET: OFFSET+LIMIT]
        users_serializer = UserProfileSerializer(users, many=True, context={'request': request})
        return Response({
            'users': users_serializer.data, 
            'has_next_page': has_next_page,
            'has_prev_page': has_prev_page
        }, status.HTTP_200_OK)
    else:
        errors.append('User not authenticated')
        return Response({"detail": "Not Authenticated", "errors": errors}, status.HTTP_401_UNAUTHORIZED)
