from decimal import Decimal
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
import factory
from realestate.listing.forms import ContactForm, SearchForm, ListingContactForm
from realestate.listing.models import Listing, Agent, Attribute
from realestate.listing.templatetags.extra_functions import currency
from realestate.listing.utils import validation_simple, validation_integer, validation_yesno, validation_decimal, \
    import_validator, validate_attribute_value


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


class ListingFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Listing

    title = 'A New House'
    slug = 'a-new-house'
    type = 'house'
    active = True
    featured = True
    baths = 2
    beds = 3
    description = 'House Description Here'
    price = Decimal('1000.00')
    agent = factory.SubFactory(AgentFactory)


class AttributeFactory(factory.Factory):
    class Meta:
        model = Attribute

    name = 'Test Attribute'
    validation = 'realestate.listing.utils.validation_simple'


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
        form.send_email()


class ViewsTests(TestCase):
    def test_listing_view(self):
        listing = ListingFactory()
        response = self.client.get(reverse('property_details', args=[listing.slug]))
        self.assertEqual(200, response.status_code)


class UtilsTests(TestCase):
    def test_validation_simple(self):
        valid, value, message = validation_simple('Hi')
        self.assertTrue(valid)
        self.assertEqual('Hi', value)
        self.assertEqual('', message)

        valid, value, message = validation_simple(None)
        self.assertFalse(valid)
        self.assertEqual(None, value)
        self.assertNotEqual('', message)

        valid, value, message = validation_simple('')
        self.assertFalse(valid)
        self.assertEqual('', value)
        self.assertNotEqual('', message)

    def test_validation_integer(self):
        valid, value, message = validation_integer(1)
        self.assertTrue(valid)
        self.assertEqual(1, value)
        self.assertEqual('', message)

        valid, value, message = validation_integer(None)
        self.assertFalse(valid)
        self.assertEqual(None, value)
        self.assertNotEqual('', message)

    def test_validation_yesno(self):
        valid, value, message = validation_yesno('yes')
        self.assertTrue(valid)
        self.assertEqual('Yes', value)
        self.assertEqual('', message)

        valid, value, message = validation_yesno(None)
        self.assertFalse(valid)
        self.assertEqual(None, value)
        self.assertNotEqual('', message)

    def test_validation_decimal(self):
        valid, value, message = validation_decimal(1.0)
        self.assertTrue(valid)
        self.assertEqual(1, value)
        self.assertEqual('', message)

        valid, value, message = validation_decimal(None)
        self.assertFalse(valid)
        self.assertEqual(None, value)
        self.assertNotEqual('', message)

    def test_import_validator(self):
        attribute = AttributeFactory.build()
        self.assertIsNotNone(import_validator(attribute.validation))
        self.assertRaises(ImportError, lambda: import_validator('fake.validator'))


    def test_validate_attribute_value(self):
        listing = ListingFactory()
        attribute = AttributeFactory.build()
        validate_attribute_value(attribute, 'Hi', listing)

    def test_currency(self):
        result = currency(1)
        self.assertEqual("$1", result)
        result = currency(None)
        self.assertEqual("$0", result)
