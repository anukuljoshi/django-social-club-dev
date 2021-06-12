
from rest_framework import serializers

from ..models import Downvote, Post, Upvote
from users.api import serializers as user_serializer


class PostSerializer(serializers.ModelSerializer):
    user = user_serializer.UserProfileSerializer()
    votes = serializers.ReadOnlyField()
    upvoted_by_user = serializers.SerializerMethodField()
    downvoted_by_user = serializers.SerializerMethodField()
    class Meta:
        model = Post
        fields = [
            'id',
            'user',
            'content',
            'createdAt',
            'updatedAt',
            'upvoted_by',
            'downvoted_by',
            'votes',
            'upvoted_by_user',
            'downvoted_by_user'
        ]
        read_only_fields = ['user', 'upvoted_by', 'downvoted_by', 'upvoted_by_user', 'downvoted_by_user']


    def get_upvoted_by_user(self, instance):
        request = self.context.get('request')
        if(request and request.user in instance.upvoted_by.all()):
            return True
        return False

    def get_downvoted_by_user(self, instance):
        request = self.context.get('request')
        if(request and request.user in instance.downvoted_by.all()):
            return True
        return False


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['content']


class UpvoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Upvote
        fields = '__all__'


class DownvoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Downvote
        fields = '__all__'