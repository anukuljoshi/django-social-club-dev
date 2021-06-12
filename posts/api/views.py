from datetime import timedelta
from users.models import Follow

from django.db.models import Count
from django.contrib.auth import get_user_model
from django.utils import timezone

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from ..models import Post, Upvote, Downvote, User
from .serializers import PostSerializer, PostCreateSerializer

User = get_user_model()

POST_PER_PAGE = 2

# get post list
@api_view(['GET'])
def following_post_list(request, *args, **kwargs):
    errors = []
    if(request.user.is_authenticated):
        page_number = int(request.query_params.get('page', 1))
        OFFSET = POST_PER_PAGE*(page_number-1)
        LIMIT = POST_PER_PAGE
        following_users = request.user.following.all().values_list('following_user_id', flat=True)
        TOTAL = Post.objects.filter(user__in=following_users).count()
        has_next_page = False
        has_prev_page = False
        if(OFFSET+LIMIT<TOTAL):
            has_next_page = True
        if(OFFSET+LIMIT>POST_PER_PAGE):
            has_prev_page = True

        posts = Post.objects.filter(user__in=following_users)[OFFSET: OFFSET+LIMIT]
        posts_serializer = PostSerializer(posts, many=True, context={'request': request})
        return Response({
            'posts': posts_serializer.data, 
            'has_next_page': has_next_page,
            'has_prev_page': has_prev_page
        }, status.HTTP_200_OK)
    errors.append('User not authenticated')
    return Response({"detail": "Not Authenticated", "errors": errors}, status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
def all_post_list(request, *args, **kwargs):
    errors = []
    if(request.user.is_authenticated):
        page_number = int(request.query_params.get('page', 1))
        OFFSET = POST_PER_PAGE*(page_number-1)
        LIMIT = POST_PER_PAGE
        TOTAL = Post.objects.all().count()
        has_next_page = False
        has_prev_page = False
        if(OFFSET+LIMIT<TOTAL):
            has_next_page = True
        if(OFFSET+LIMIT>POST_PER_PAGE):
            has_prev_page = True

        posts = Post.objects.all()[OFFSET: OFFSET+LIMIT]
        posts_serializer = PostSerializer(posts, many=True, context={'request': request})
        return Response({
            'posts': posts_serializer.data, 
            'has_next_page': has_next_page,
            'has_prev_page': has_prev_page
        }, status.HTTP_200_OK)
    errors.append('User not authenticated')
    return Response({"detail": "Not Authenticated", "errors": errors}, status.HTTP_401_UNAUTHORIZED)


# get a post detail
@api_view(['GET'])
def post_detail(request, *args, **kwargs):
    errors = []
    if(request.user.is_authenticated):
        postId = kwargs.get('postId')
        post = Post.objects.filter(pk=postId).first()
        if(not post):
            errors.append('Post not found.')
            return Response({'detail': 'Not found', 'errors': errors}, status=status.HTTP_404_NOT_FOUND)
        post_serializer = PostSerializer(post, context={'request': request})
        return Response(post_serializer.data, status.HTTP_200_OK)
    errors.append('User not authenticated')
    return Response({"detail": "Not Authenticated", "errors": errors}, status.HTTP_401_UNAUTHORIZED)


# createa a post
@api_view(['POST'])
def post_create(request, *args, **kwargs):
    errors = []
    if(request.user.is_authenticated):
        post_serializer = PostCreateSerializer(data=request.data)
        if(post_serializer.is_valid()):
            post_serializer.save(user=request.user)
            return Response(post_serializer.data, status.HTTP_201_CREATED)
        errors.append('Something went wrong. Try again.')
        return Response({"detail": "Post creation failed", "errors": errors }, status.HTTP_400_BAD_REQUEST)
    errors.append('User not authenticated')
    return Response({"detail": "Not Authenticated", "errors": errors}, status.HTTP_401_UNAUTHORIZED)


# delete a post
@api_view(['DELETE'])
def post_delete(request, *args, **kwargs):
    errors = []
    if(request.user.is_authenticated):
        postId = kwargs.get('postId')
        post = Post.objects.filter(pk=postId).first()
        if(not post):
            errors.append('Post not found.')
            return Response({'detail': 'Not found', 'errors': errors}, status=status.HTTP_404_NOT_FOUND)
        if(post.user==request.user):
            post.delete()
            return Response({}, status.HTTP_204_NO_CONTENT)
        errors.append('User not authorized')
        return Response({"detail": "Not Authorized", "errors": errors}, status.HTTP_403_FORBIDDEN)
    errors.append('User not authenticated')
    return Response({"detail": "Not Authenticated", "errors": errors}, status.HTTP_401_UNAUTHORIZED)


# upvote/downvote a post
@api_view(['POST'])
def post_vote(request, *args, **kwargs):
    errors = []
    if(request.user.is_authenticated):
        postId = request.data.get('postId')
        vote_type = request.data.get('vote_type')
        post = Post.objects.filter(pk=postId).first()
        if(not post):
            errors.append('Post not found.')
            return Response({'detail': 'Not found', 'errors': errors}, status=status.HTTP_404_NOT_FOUND)
        if(vote_type=='UPVOTE'):
            downvote = Downvote.objects.filter(user=request.user, post=post).first()
            if(downvote):
                downvote.delete()
            upvote, created = Upvote.objects.get_or_create(user=request.user, post=post)
            if(not created):
                upvote.delete()
            return Response({"detail": "upvoted"}, status=status.HTTP_200_OK)
        elif(vote_type=='DOWNVOTE'):
            upvote = Upvote.objects.filter(user=request.user, post=post).first()
            if(upvote):
                upvote.delete()
            downvote, created = Downvote.objects.get_or_create(user=request.user, post=post)
            if(not created):
                downvote.delete()
            return Response({"detail": "upvoted"}, status=status.HTTP_200_OK)
    errors.append('User not authenticated')
    return Response({"detail": "Not Authenticated", "errors": errors}, status.HTTP_401_UNAUTHORIZED)


# get list of popular post
@api_view(['GET'])
def post_popular(request, *args, **kwargs):
    errors = []
    if(request.user.is_authenticated):
        this_hour = timezone.now().replace(minute=0, second=0, microsecond=0)
        one_hour_later = this_hour + timedelta(hours=1)
        upvotes = Upvote.objects.annotate(vote_count=Count('user')).filter(createdAt__range=(this_hour, one_hour_later))
        vote_counts = {}
        count = 0
        for upvote in upvotes:
            if not vote_counts.get(upvote.post.id):
                vote_counts[upvote.post.id] = 1
            else:
                vote_counts[upvote.post.id] += 1
        vote_sorted_post = sorted(vote_counts, key=vote_counts.get, reverse=True)
        popular_posts = list(Post.objects.filter(pk__in=vote_sorted_post))
        popular_posts.sort(key=lambda post: vote_sorted_post.index(post.id))
        post_serializer = PostSerializer(popular_posts, many=True, context={'request': request})
        return Response(post_serializer.data, status=status.HTTP_200_OK)
    errors.append('User not authenticated')
    return Response({"detail": "Not Authenticated", "errors": errors}, status.HTTP_401_UNAUTHORIZED)
