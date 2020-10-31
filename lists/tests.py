from django.test import TestCase
from django.urls import resolve
from lists.views import home_page
from django.http import HttpRequest


class TestHomePage(TestCase):
    """Test home page"""

    def test_url_resolves_to_home_page_view(self):
        """root url resolves to home page view"""
        found = resolve("/")
        self.assertEqual(found.func, home_page)

    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')
