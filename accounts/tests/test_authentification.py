from django.test import TestCase
from django.contrib.auth import get_user_model
from django.test.client import RequestFactory
from accounts.authentification import PasswordlessAuthenticationBackend
from accounts.models import Token, User


class AuthenticateTest(TestCase):
    """тест аутентификации"""
    def setUp(self) -> None:
        rf = RequestFactory()
        self.request = rf.get('/accounts/')

    def test_returns_None_if_not_such_token(self):
        """тест: возвращается None, если нет такого маркера"""
        result = PasswordlessAuthenticationBackend().authenticate(self.request, uid='no-such-token')
        self.assertIsNone(result)

    def test_returns_new_user_with_correct_email_if_token_exists(self):
        """Возвращает нового пользователя, если токен существует"""
        email = 'edith@example.com'
        token = Token.objects.create(email=email)
        user = PasswordlessAuthenticationBackend().authenticate(self.request, uid=token.uid)
        new_user = User.objects.get(email=email)

        self.assertEqual(user, new_user)

    def test_returns_existing_user_with_correct_email_if_token_exists(self):
        """Возвращает существующего пользователя, если токен существует"""
        email = 'edith@example.com'
        token = Token.objects.create(email=email)
        existing_user = User.objects.create(email=token.email)
        user = PasswordlessAuthenticationBackend().authenticate(self.request, uid=token.uid)
        self.assertEqual(existing_user, user)


class GetUserTest(TestCase):
    """тест получения пользователя"""

    def test_gets_user_by_email(self):
        """тест получает пользователя по емайлу"""
        User.objects.create(email='some@example.com')
        desired_user = User.objects.create(email='edith@example.com')
        found_user = PasswordlessAuthenticationBackend().get_user('edith@example.com')
        self.assertEqual(desired_user, found_user)

    def test_returns_None_if_no_user_with_that_email(self):
        self.assertIsNone(
            PasswordlessAuthenticationBackend().get_user('edith@example')
        )
