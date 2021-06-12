from django.contrib.auth import get_user_model

from rest_framework import authentication

User = get_user_model()

class DevAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        user = User.objects.get(id=1)
        return (user, None)
