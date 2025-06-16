import base64

import jwt
from django.conf import settings
from django.utils import timezone
from rest_framework import authentication, exceptions

from app_user.models import User


def jwt_expire_time():
    return timezone.now() + settings.JWT_EXPIRE_TIME


class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_data = authentication.get_authorization_header(request)
        if not auth_data:
            return None

        prefix, token = auth_data.decode('utf-8').split(' ')

        try:
            payload = jwt.decode(token.strip(), base64.b64decode(settings.JWT_SECRET_KEY), algorithms=["HS256"])
            user = User.objects.get(username=payload['user_id'])
            return (user, token)
        except jwt.DecodeError as identifier:
            raise exceptions.AuthenticationFailed('Token invalide')
        except jwt.ExpiredSignatureError as identifier:
            raise exceptions.AuthenticationFailed('Token expiré')
        except jwt.InvalidSignatureError as identifier:
            raise exceptions.AuthenticationFailed('Token non autorisé')

        return super().authenticate(request)
