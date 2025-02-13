from django.test import TestCase
from django.urls import reverse

class Chapter4Tests(TestCase):
    def test_about_template_exists(self):
        """Test if about.html exists and is used"""
        response = self.client.get(reverse('rango:about'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'rango/about.html')

    def test_about_contains_expected_content(self):
        """Test if about page contains expected content"""
        response = self.client.get(reverse('rango:about'))
        self.assertContains(response, "Rango says...")
        self.assertContains(response, "Here is the about page.")
        self.assertContains(response, "This tutorial has been put together by")

    def test_about_static_image_exists(self):
        """Test if about.html includes the static image"""
        response = self.client.get(reverse('rango:about'))
        self.assertContains(response, 'src="/static/images/rango.jpg"')

    def test_about_media_image_exists(self):
        """Test if about.html includes the media image"""
        response = self.client.get(reverse('rango:about'))
        self.assertContains(response, 'src="/media/cat.jpg"')
