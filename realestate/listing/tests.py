from django.contrib.auth.models import User
from django.test import TestCase
import factory
from realestate.listing.forms import ContactForm, SearchForm, ListingContactForm
from realestate.listing.models import Listing, Agent


class UserFactory(factory.Factory):
    class Meta:
        model = User

    first_name = 'Agent'
    last_name = '007'
    email = factory.LazyAttribute(lambda a: '{0}.{1}@example.com'.format(a.first_name, a.last_name).lower())


class AgentFactory(factory.Factory):
    class Meta:
        model = Agent

    first_name = 'Agent'
    last_name = '007'
    user = factory.SubFactory(UserFactory)


class ListingFactory(factory.Factory):
    class Meta:
        model = Listing

    title = 'A New House'
    description = 'House Description Here'
    price = 0
    agent = factory.SubFactory(AgentFactory)


class FormTests(TestCase):
    def test_listingcontact_form(self):
        form_data = {
            'name': 'Williams Mendez',
            'email': 'test@example.com',
            'phone': '8090000000',
            'message': 'Test message',
        }

        form = ListingContactForm(data=form_data)
        self.assertEqual(form.is_valid(), True)

        listing = ListingFactory.build()
        form.send_contact_form(listing)

    def test_search_form(self):
        form_data = {}

        form = SearchForm(data=form_data)
        self.assertEqual(form.is_valid(), True)

    def test_contact_form(self):
        form_data = {
            'name': 'Williams Mendez',
            'subject': 'Testing Form',
            'email': 'test@example.com',
            'message': 'This is a simple test.',
        }
        form = ContactForm(data=form_data)
        self.assertEqual(form.is_valid(), True)