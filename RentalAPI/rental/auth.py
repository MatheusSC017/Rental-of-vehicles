from django.conf import settings
from rest_framework import authentication
from rest_framework import exceptions


class Authenticated:
    is_authenticated = True


class MessagingSystemAccessTokenAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        token = request.META.get('HTTP_AUTHORIZATION')
        if not token:
            return None

        if token != settings.MESSAGING_SYSTEM_ACCESS_TOKEN:
            raise exceptions.AuthenticationFailed('Invalid token')

        return Authenticated(), None
