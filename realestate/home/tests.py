from django.core.urlresolvers import reverse
from django.test import TestCase


class ViewsTests(TestCase):
    def test_index_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(200, response.status_code)

    def test_contact_view(self):
        response = self.client.get(reverse('home_contact'))
        self.assertEqual(200, response.status_code)