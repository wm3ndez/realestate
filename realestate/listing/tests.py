from django.test import TestCase
from realestate.listing.forms import ContactForm


class FormTests(TestCase):
    def test_contact_form(self):
        form_data = {
            'name': 'Williams Mendez',
            'subject': 'Testing Form',
            'email': 'test@example.com',
            'message': 'This is a simple test.',
        }
        form = ContactForm(data=form_data)
        self.assertEqual(form.is_valid(), True)