from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

from rest_framework import serializers

from ..models import Profile, Follow

User = get_user_model()


class FollowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = [
            'id',
            'user_id',
            'createdAt'
        ]


class FollowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = [
            'id',
            'following_user_id',
            'createdAt'
        ]


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            'id', 
            'bio', 
            'display_name',
        ]
        read_only_fields = ['id']



class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    profile = ProfileSerializer()
    followers = serializers.SerializerMethodField()
    following = serializers.SerializerMethodField()
    followed_by_user = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = [
            'id', 
            'username', 
            'email',
            'profile', 
            'password', 
            'followers',
            'following',
            'followed_by_user'
        ]


    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        return super().create(validated_data)


    def get_following(self, instance):
        return FollowingSerializer(instance.following.all(), many=True).data


    def get_followers(self, instance):
        return FollowerSerializer(instance.followers.all(), many=True).data


    def get_followed_by_user(self, instance):
        request = self.context.get('request')
        user = request.user
        # print(instance.followers.filter(user_id=user))
        if(instance.followers.filter(user_id=user)):
            return True
        return False


class UserProfileSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    profile = ProfileSerializer()
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    followed_by_user = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = [
            'id', 
            'username', 
            'email',
            'profile', 
            'password', 
            'followed_by_user',
            'followers_count',
            'following_count'
        ]


    # def create(self, validated_data):
    #     validated_data['password'] = make_password(validated_data.get('password'))
    #     return super().create(validated_data)


    def get_following_count(self, instance):
        return instance.following.all().count()


    def get_followers_count(self, instance):
        return instance.followers.all().count()


    def get_followed_by_user(self, instance):
        request = self.context.get('request')
        user = request.user
        # print(instance.followers.filter(user_id=user))
        if(instance.followers.filter(user_id=user)):
            return True
        return False


class UserUpdateSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'profile',
        ]