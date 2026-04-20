from django.test import TestCase
from django.urls import resolve
from lists.views import home_page
from django.http import HttpRequest
from django.template.loader import render_to_string

class HomePageTest(TestCase):

    def test_home_page_template_uses_correct_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

# Create your tests here.
