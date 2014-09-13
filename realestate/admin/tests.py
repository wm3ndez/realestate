from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from realestate.listing.tests import ListingFactory

listing_info = {
    'title': 'Test Title',
    'description': 'Test Description',
    'price': 0,
    'price_currency': 'DOP',
    'type': 'house',
    'offer': 'buy-rent',
    'active': True,
    'featured': True,
}


class AdminViewsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('test', 'test@example.com', 'test')
        self.user.is_staff = True
        self.user.save()
        self.client.login(username=self.user.username, password='test')
        self.listing = ListingFactory.build()


    def test_listings_view(self):
        response = self.client.get(reverse('admin-list-listing'))
        self.assertEqual(200, response.status_code)

    def test_create_listing_view(self):
        response = self.client.get(reverse('add-listing-wizard', args=['listingdata']))
        self.assertEqual(200, response.status_code)

        # response = self.client.post(reverse('add-listing'), data=listing_info)
        # self.assertEqual(200, response.status_code)

        # def test_update_listing_view(self):
        # listing = ListingFactory.create()
        # response = self.client.get(reverse('update-listing', args=[listing.id]), data=listing_info)
        # self.assertEqual(200, response.status_code)
        #
        # response = self.client.post(reverse('update-listing', args=[listing.id]), data=listing_info)
        # self.assertEqual(200, response.status_code)

    def test_agent_list_view(self):
        response = self.client.get(reverse('admin-list-agents'))
        self.assertEqual(200, response.status_code)

    def test_contact_list_view(self):
        response = self.client.get(reverse('admin-list-contacts'))
        self.assertEqual(200, response.status_code)

    def test_location_list_view(self):
        response = self.client.get(reverse('admin-list-sectors'))
        self.assertEqual(200, response.status_code)

    def test_deals_list_view(self):
        response = self.client.get(reverse('admin-list-deals'))
        self.assertEqual(200, response.status_code)

    # def test_apikey_list_view(self):
    # response = self.client.get(reverse('admin-api-keys'))
    # self.assertEqual(200, response.status_code)

    def test_users_list_view(self):
        self.user.is_superuser = True
        self.user.save()

        response = self.client.get(reverse('admin-list-users'))
        self.assertEqual(200, response.status_code)
