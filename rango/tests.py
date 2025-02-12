from django.test import TestCase
from django.urls import reverse

class RangoViewTests(TestCase):

    def test_index_view_exists(self):
        """
        test if index view exists
        """
        response = self.client.get(reverse('rango:index'))
        self.assertEqual(response.status_code, 200)

    def test_about_view_exists(self):
        """
        test if about view exists
        """
        response = self.client.get(reverse('rango:about'))
        self.assertEqual(response.status_code, 200)



