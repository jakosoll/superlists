from django.test import TestCase
from unittest.mock import patch, call
from accounts.models import Token


class SendLoginEmailViewTest(TestCase):
    """тест представления, которое отправляет email
    для входа в систему"""

    def test_redirects_to_home_page(self):
        """тест: после отправки емайла переадресовывается на
        домашнюю страницу"""
        response = self.client.post('/accounts/send_login_email', data={'email': 'edith@example.com'})
        self.assertRedirects(response, '/')

    @patch('accounts.views.send_mail')
    def test_sends_email_to_address_from_post(self, mock_send_mail):
        """тест: отправление сообщения на адрес из метода post"""

        self.client.post('/accounts/send_login_email', data={'email': 'edith@example.com'})

        self.assertTrue(mock_send_mail.called)

        (subject, body, from_email, to_list), kwargs = mock_send_mail.call_args

        self.assertEqual(subject, 'Your login link for Superlists')
        self.assertEqual(from_email, 'noreply@superlists')
        self.assertEqual(to_list, ['edith@example.com'])

    def test_add_success_message(self):
        """тест: добавляется сообщение об успехе"""
        response = self.client.post('/accounts/send_login_email', data={'email': 'edith@@example.com'}, follow=True)

        message = list(response.context['messages'])[0]

        self.assertEqual(message.message, 'Проверьте свою почту, мы отправили вам ссылку, которую можно'
                                          'использовать для входа на сайт')
        self.assertEqual(message.tags, 'success')

    def test_creates_token_associated_with_email(self):
        """тест: создается маркер, связанный с электронной почтой"""
        self.client.post('/accounts/send_login_email', data={'email': 'edith@exapmle.com'})
        token = Token.objects.first()
        self.assertEqual(token.email, 'edith@exapmle.com')

    @patch('accounts.views.send_mail')
    def test_sends_link_to_login_using_token_uid(self, mock_send_mail):
        """тест: ссылка отправляется посльзователю"""
        self.client.post('/accounts/send_login_email', data={'email': 'edith@example.com'})

        token = Token.objects.first()
        expected_url = f'http://testserver/accounts/login?token={token.uid}'
        (subject, body, from_email, to_list), kwargs = mock_send_mail.call_args
        self.assertIn(expected_url, body)


@patch('accounts.views.auth')
class LoginViewTest(TestCase):
    """тест представления входа в систему"""

    def test_redirects_to_home_page(self, mock_auth):
        """тест: представление переадресовывает на домашнюю страницу"""
        response = self.client.get('/accounts/login?token=abcd123')
        self.assertRedirects(response, '/')

    def test_calls_authenticate_with_uid_from_get_request(self, mock_auth):
        """тест: вызывается authenticate с uid из GET-запроса"""
        response = self.client.get('/accounts/login?token=abcd123')
        self.assertEqual(
            mock_auth.authenticate.call_args,
            call(response.wsgi_request, uid='abcd123')
        )

    def test_calls_auth_login_with_user_if_there_is_one(self, mock_auth):
        """тест: вызывается authenticate с пользователем, если такой имеется"""
        response = self.client.get('/accounts/login?token=abcd123')
        self.assertEqual(
            mock_auth.login.call_args,
            call(response.wsgi_request, mock_auth.authenticate.return_value)
        )

    def test_does_not_login_if_user_is_not_authenticated(self, mock_auth):
        """тест: не регистируется в системе если пользователь не аутентифицирован"""
        mock_auth.authenticate.return_value = None  # устанавлием None в явном виде, т.к. mock не вернет None
        self.client.get('/accounts/login?token=abcd123')
        self.assertEqual(mock_auth.login.called, False)


@patch('accounts.views.auth')
class LogoutTest(TestCase):
    """Тестирование выхода"""
    def test_redirects_to_home_page_after_logout(self, mock_auth):
        """Редирект на домашнюю страницу после выхода"""
        response = self.client.get('/accounts/logout')
        self.assertRedirects(response, '/')

    def test_calls_logout_(self, mock_auth):
        """Тест: фукнция вызывается"""
        response = self.client.get('/accounts/logout')
        self.assertEqual(
            mock_auth.logout.called, True
        )

