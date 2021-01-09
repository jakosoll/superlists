import sys
from django.contrib.auth.backends import BaseBackend
from accounts.models import Token, User


class PasswordlessAuthenticationBackend(BaseBackend):

    def authenticate(self, request, **kwargs):
        """аутентификация"""
        uid = kwargs['uid']
        try:
            token = Token.objects.get(uid=uid)
            return User.objects.get(email=token.email)
        except User.DoesNotExist:
            return User.objects.create(email=token.email)
        except Token.DoesNotExist:
            return None

    def get_user(self, email):
        """return user if exists"""
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return None
