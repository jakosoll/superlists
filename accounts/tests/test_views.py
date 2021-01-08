from django.test import TestCase
from unittest.mock import patch
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


class LoginViewTest(TestCase):
    """тест представления входа в систему"""

    def test_redirects_to_home_page(self):
        """тест: представление переадресовывает на домашнюю страницу"""
        response = self.client.get('/accounts/login?token=abc123')
        self.assertRedirects(response, '/')
