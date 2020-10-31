from django.test import TestCase
from django.urls import resolve
from lists.views import home_page


class TestHomePage(TestCase):
    """Test home page"""

    def test_url_resolves_to_home_page_view(self):
        """root url resolves to home page view"""
        found = resolve("/")
        self.assertEqual(found.func, home_page)
# Create your tests here.
