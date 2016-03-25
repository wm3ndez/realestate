from decimal import Decimal

import factory
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.test import TestCase
from realestate.listing.forms import ContactForm, ListingContactForm
from realestate.listing.models import Listing, Agent, Attribute, Location, AttributeListing
from realestate.listing.templatetags.extra_functions import currency
from realestate.listing.utils import validation_simple, validation_integer, validation_yesno, validation_decimal, \
    import_validator, validate_attribute_value


class SiteFactory(factory.Factory):
    class Meta:
        model = Site

    domain = 'www.example.com'
    name = 'Real Estate'


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = User

    first_name = 'Agent'
    last_name = '007'
    email = factory.LazyAttribute(lambda a: '{0}.{1}@example.com'.format(a.first_name, a.last_name).lower())
    username = factory.Sequence(lambda n: 'person{0}'.format(n))


class AgentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Agent

    first_name = 'Agent'
    last_name = '007'
    email = factory.Sequence(lambda n: 'person{0}@example.com'.format(n))
    user = factory.SubFactory(UserFactory)


class LocationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Location

    name = 'Test Location'
    location_type = 'state'


class ListingFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Listing

    title = 'A New House'
    slug = 'a-new-house'
    type = 'house'
    offer = 'buy-rent'
    active = True
    featured = True
    baths = 2
    beds = 3
    description = 'House Description Here'
    price = Decimal('1000.00')
    agent = factory.SubFactory(AgentFactory)
    location = factory.SubFactory(LocationFactory)


class AttributeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Attribute

    name = 'Test Attribute'
    validation = 'realestate.listing.utils.validation_simple'


class AttributeListingFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AttributeListing

    listing = factory.SubFactory(ListingFactory)
    attribute = factory.SubFactory(AttributeFactory)
    value = 'Test'


class FormTests(TestCase):
    def setUp(self):
        SiteFactory.create()

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
        listing = ListingFactory.create()
        response = self.client.get(reverse('property_details', args=[listing.slug]))
        self.assertEqual(200, response.status_code)

    def test_map_view(self):
        response = self.client.get(reverse('listings-map'), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(200, response.status_code)

    def test_for_sale_view(self):
        response = self.client.get(reverse('properties_for_sale'))
        self.assertEqual(200, response.status_code)

    def test_for_rent_view(self):
        response = self.client.get(reverse('properties_for_rent'))
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
        self.assertIsNotNone(import_validator('validate_attribute_value'))
        self.assertRaises(ImportError, lambda: import_validator('fake.validator'))
        self.assertRaises(ImportError, lambda: import_validator('fake'))
        self.assertRaises(ImportError, lambda: import_validator(None))

    def test_validate_attribute_value(self):
        listing = ListingFactory()
        attribute = AttributeFactory.build()
        validate_attribute_value(attribute, 'Hi', listing)

    def test_currency(self):
        result = currency(1)
        self.assertEqual("$1", result)
        result = currency(None)
        self.assertEqual("$0", result)


class ModelTests(TestCase):
    def setUp(self):
        self.listing = ListingFactory()

    def test_listing(self):
        self.assertEqual(0, self.listing.suggested.count())
        self.assertTrue(self.listing.should_have_baths)
        self.assertTrue(self.listing.should_have_beds)
        self.assertEqual(0, self.listing.nearby.count())
        self.assertEqual(0, len(self.listing.image_list))
        self.assertFalse(self.listing.on_sale)
        self.assertIsNotNone(self.listing.code)
        self.assertIsNone(self.listing.main_image)

    def test_attribute_listing(self):
        attributelisting = AttributeListingFactory.create()
        self.assertEqual("A New House", attributelisting.listing.title)

        AttributeListingFactory.create(listing=attributelisting.listing,
                                       attribute__validation='realestate.listing.utils.validation_yesno')
        AttributeListingFactory.create(listing=attributelisting.listing, value=1,
                                       attribute__validation='realestate.listing.utils.validation_integer')
        AttributeListingFactory.create(listing=attributelisting.listing, value=10.0,
                                       attribute__validation='realestate.listing.utils.validation_decimal')

        features = attributelisting.listing.get_features()
        self.assertEqual(4, len(features))

    def test_location(self):
        self.assertEqual(0, Location.objects.streets().count())
        self.assertEqual(0, Location.objects.sectors().count())
        self.assertEqual(0, Location.objects.cities().count())
        self.assertEqual(1, Location.objects.states().count())

        self.assertIn(self.listing.location.name, self.listing.location.get_parent_name(self.listing.location, []))
