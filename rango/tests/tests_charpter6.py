from django.test import TestCase
from django.urls import reverse
from rango.models import Category, Page
from django.utils.text import slugify

class Chapter6Tests(TestCase):

    def setUp(self):
        """ Set up test data for categories and pages """
        self.category = Category.objects.create(name="Python", slug=slugify("Python"), views=128, likes=64)
        self.page1 = Page.objects.create(category=self.category, title="Official Python Tutorial", url="http://docs.python.org/3/tutorial/", views=100)
        self.page2 = Page.objects.create(category=self.category, title="Learn Python in 10 Minutes", url="http://www.korokithakis.net/tutorials/python/", views=50)

    def test_category_slug_creation(self):
        """ Test that slug is correctly generated for Category """
        self.assertEqual(self.category.slug, "python", "Slug was not correctly generated.")

    def test_index_view_displays_top_categories(self):
        """ Test that the index view displays top categories """
        response = self.client.get(reverse('rango:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Python")

    def test_category_page_exists(self):
        """ Test that the category page for Python exists """
        response = self.client.get(reverse('rango:show_category', kwargs={'category_name_slug': self.category.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Python")

    def test_category_page_shows_associated_pages(self):
        """ Test that the category page lists associated pages """
        response = self.client.get(reverse('rango:show_category', kwargs={'category_name_slug': self.category.slug}))
        self.assertContains(response, "Official Python Tutorial")
        self.assertContains(response, "Learn Python in 10 Minutes")

    def test_invalid_category_shows_error_message(self):
        """ Test that an invalid category page shows an error message """
        response = self.client.get(reverse('rango:show_category', kwargs={'category_name_slug': 'non-existent'}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "The specified category does not exist.")
