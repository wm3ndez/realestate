# -*- coding: utf-8 -*-
from decimal import Decimal

import os
import re
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.template.defaultfilters import slugify
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from djmoney.models.fields import MoneyField
from moneyed import USD, Money
from realestate.home.models import Contact
from sorl.thumbnail import ImageField

TYPES = (
    ('house', _('Houses')),
    ('villa', _('Villas')),
    ('penthouse', _('Penthouses')),
    ('apartment', _('Apartments')),
    ('residencial-land', _('Residential Land')),
    ('corporate-office', _('Corporate Offices')),
    ('commercial-office', _('Commercial Offices')),
    ('commercial-space', _('Commercial Space')),
    ('industrial-building', _('Industrial Buildings')),
    ('commercial-warehouses', _('Commercial Warehouses')),
    ('commercial-land', _('Commercial Land')),
)

LOCATION_STREET = 'street'
LOCATION_SECTOR = 'sector'
LOCATION_CITY = 'city'
LOCATION_STATE = 'state'

LOCATION_TYPES = (
    (LOCATION_STREET, _('Street')),
    (LOCATION_SECTOR, _('Sector')),
    (LOCATION_CITY, _('City')),
    (LOCATION_STATE, _('State/Province')),
)

OFFERS = (
    ('buy', _('For Sale')),
    ('rent', _('For Rent')),
    ('buy-rent', _('For Sale/For Rent'))
)

VALIDATIONS = [
    ('realestate.listing.utils.validation_simple', _('One or more characters')),
    ('realestate.listing.utils.validation_integer', _('Integer')),
    ('realestate.listing.utils.validation_yesno', _('Yes/No')),
    ('realestate.listing.utils.validation_decimal', _('Decimal')),
]


class LocationManager(models.Manager):
    def states(self, **kwargs):
        return self.filter(location_type=LOCATION_STATE, **kwargs)

    def cities(self, **kwargs):
        return self.filter(location_type=LOCATION_CITY, **kwargs)

    def sectors(self, **kwargs):
        return self.filter(location_type=LOCATION_SECTOR, **kwargs)

    def streets(self, **kwargs):
        return self.filter(location_type=LOCATION_STREET, **kwargs)


class Location(models.Model):
    parent = models.ForeignKey('self', verbose_name=_('Location'), null=True,
                               blank=True)
    name = models.CharField(_('Name'), max_length=60)
    location_type = models.CharField(_('Location Type'),
                                     choices=LOCATION_TYPES,
                                     default=LOCATION_SECTOR, max_length=20)

    objects = LocationManager()

    def __unicode__(self):
        location_tree = self.get_parent_name(self, [])
        return ', '.join(location_tree)

    def __str__(self):
        return self.__unicode__()

    def get_parent_name(self, location, names):
        names.append(location.name)
        if location.parent is None:
            return names
        return self.get_parent_name(location.parent, names)


class AgentManager(models.Manager):
    def active(self, **kwargs):
        return self.filter(active=True, **kwargs)

    def with_listings(self, **kwargs):
        return self.active(listing__isnull=False, **kwargs)


class Agent(models.Model):
    first_name = models.CharField(max_length=30, verbose_name=_('First name'))
    last_name = models.CharField(max_length=30, verbose_name=_('Last name'))
    phone = models.CharField(max_length=15, verbose_name=_('Phone'), null=True, blank=True)
    mobile = models.CharField(max_length=15, verbose_name=_('Cellphone'), null=True, blank=True)
    location = models.ForeignKey(Location, verbose_name=_('Location'), null=True, blank=True)
    address = models.CharField(max_length=200, verbose_name=_('Address'), null=True, blank=True)
    image = ImageField(upload_to='agents/', default='', verbose_name=_('Picture'), null=True, blank=True)
    user = models.OneToOneField(User, verbose_name=_('User'), null=True, blank=True)
    active = models.BooleanField(default=False, verbose_name=_('Active'))

    objects = AgentManager()

    @property
    def name(self):
        return '%s %s' % (self.first_name, self.last_name)

    @property
    def email(self):
        return self.user.email if self.user is not None else None

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('Agent')
        verbose_name_plural = _('Agents')


class ListingManager(models.Manager):
    def active(self, **kwargs):
        return self.filter(active=True, **kwargs)

    def featured(self, **kwargs):
        return self.active().filter(featured=True)

    def rent(self, **kwargs):
        return self.active().filter(offer__in=('buy-rent', 'rent'))

    def sale(self, **kwargs):
        return self.active().filter(offer__in=('buy-rent', 'buy'))


class Listing(models.Model):
    title = models.CharField(max_length=100, verbose_name=_('Title'))
    slug = models.SlugField(max_length=100, unique=True, blank=False, verbose_name=_('Slug'))
    description = models.TextField(verbose_name=_('Description'), null=True, blank=True)
    price = MoneyField(default=Money(0, USD), max_digits=12, decimal_places=2, verbose_name=_('Price'))
    location = models.ForeignKey(Location, null=True, blank=True)
    type = models.CharField(_('Listing Type'), max_length=30, choices=TYPES)
    offer = models.CharField(max_length=10, choices=OFFERS, verbose_name=_('Offer'))
    active = models.BooleanField(_('Active'), default=False)
    featured = models.BooleanField(default=False, verbose_name=_('Featured'))
    baths = models.PositiveIntegerField(_('Bathrooms'), default=0, null=True, blank=True)
    beds = models.PositiveIntegerField(_('Bedrooms'), default=0, null=True, blank=True)
    size = models.PositiveIntegerField(_('Size(m2)'), default=0, null=True, blank=True)
    coords = models.CharField(max_length=255, default='19.000000,-70.400000', verbose_name=_('Coords'), null=True,
                              blank=True)
    agent = models.ForeignKey(Agent, null=True, blank=True, verbose_name=_('Agent'))
    contact = models.ForeignKey(Contact, null=True, blank=True)
    notes = models.TextField(max_length=500, verbose_name=_('Private Notes'), null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created'))
    last_modified = models.DateTimeField(auto_now=True, verbose_name=_('Last Modified'))

    objects = ListingManager()

    @property
    def main_image(self):
        im = self.images.all()
        if im.count():
            return im[0]
        return None

    @property
    def image_list(self):
        return [{'title': image.name, 'url': image.absolute_url, 'order': image.order} for image in self.images.all()]

    @property
    def address(self):
        return self.get_address()

    def get_address(self):
        if self.location is None:
            return _('No location provided')
        return self.location

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _('Listing')
        verbose_name_plural = _('Listings')
        ordering = ['-pk', ]

    def save(self, **kwargs):
        self._generate_valid_slug()
        super(Listing, self).save(**kwargs)

    def _generate_valid_slug(self):
        if not self.is_valid_slug():
            slug = slugify(self.title)
            while Listing.objects.filter(slug=slug).exclude(id=self.id).exists():
                slug_parts = slug.split('-')
                if slug_parts[-1].isdigit():
                    slug_parts[-1] = '%s' % (int(slug_parts[-1]) + 1)
                else:
                    slug_parts.append('2')
                slug = '-'.join(slug_parts)
            self.slug = slug

    def is_valid_slug(self):
        if self.slug is None or len(self.slug) < 10:
            return False
        match = re.match('[^\w\s-]', self.slug)
        if not match:
            return False
        return self.slug == slugify(self.slug)

    @property
    def absolute_url(self):
        return self.get_absolute_url()

    def get_absolute_url(self):
        return reverse('property_details', args=[self.slug])

    def get_features(self):
        attributes = []
        for attribute in self.attributelisting_set.all():
            attribute_name = _(attribute.attribute.name)
            if attribute.attribute.validation == 'realestate.listing.utils.validation_simple':
                attributes.append('{0}: {1}'.format(attribute_name, attribute.value))
            elif attribute.attribute.validation == 'realestate.listing.utils.validation_yesno':
                attributes.append(attribute_name)
            else:
                if attribute.attribute.validation == 'realestate.listing.utils.validation_integer':
                    attributes.append('{0} {1}'.format(attribute.value, attribute_name))
                else:
                    attributes.append('{0:.2f} {1}'.format(Decimal(attribute.value), attribute_name))

        return attributes

    @property
    def nearby(self):
        return Listing.objects.active(location=self.location).exclude(id=self.id).order_by('?')

    @property
    def has_baths_or_beds(self):
        return self.should_have_beds or self.should_have_baths

    @property
    def suggested(self):
        qs = Listing.objects.active(type=self.type)

        price = self.price
        lh = price * .90
        rh = price * 1.10

        if self.has_baths_or_beds:
            if self.should_have_baths:
                qs = qs.filter(baths=self.baths)
            if self.should_have_beds:
                qs = qs.filter(beds=self.beds)

            if qs.count() == 0:
                qs = Listing.objects.active(type=self.type, price__range=(lh, rh))
        else:
            qs = qs.filter(price__range=(lh, rh))

        return qs.exclude(id=self.id).order_by('?')

    @property
    def should_have_beds(self):
        return self.type in ('house', 'penthouse', 'apartment', 'villa',)

    @property
    def should_have_baths(self):
        return 'land' not in self.type

    @property
    def on_sale(self):
        return Deal.objects.on_sale(listing__in=(self,)).exists()

    @property
    def code(self):
        if self.agent is not None:
            agent = self.agent
            prefix = '{0}{1}'.format(agent.first_name[0], agent.last_name[0])
            return '{0}{1:04}'.format(prefix, self.id).upper()

        rent_or_sale = 'v' if self.offer in ('buy-rent', 'buy') else 'r'
        return '{0}{1:04x}'.format(rent_or_sale, self.id).upper()


class Attribute(models.Model):
    name = models.CharField(_('Attribute'), max_length=100)
    validation = models.CharField(_('Value type'), choices=VALIDATIONS, max_length=100)

    class Meta:
        ordering = ('name',)
        verbose_name = _('Attribute')
        verbose_name_plural = _('Attributes')

    def __unicode__(self):
        return self.__str__()

    def __str__(self):
        return self.name


class AttributeListing(models.Model):
    listing = models.ForeignKey(Listing)
    attribute = models.ForeignKey(Attribute)
    value = models.CharField(_('Value'), max_length=255)
    order = models.SmallIntegerField(_('Order'), default=99)

    class Meta:
        verbose_name = _('Listing attribute')
        verbose_name_plural = _('Listing attributes')
        ordering = ['order', ]

    def __unicode__(self):
        return '%s: %s' % (self.attribute.name, self.value)


class ListingImage(models.Model):
    listing = models.ForeignKey(Listing, related_name='images', verbose_name=_('Listing'))
    name = models.CharField(_('Name'), max_length=60)
    image = ImageField(_('Image'), upload_to='listing/')
    added = models.DateTimeField(_('Added'), auto_now_add=True)
    order = models.PositiveSmallIntegerField(_('Order'), default=99, null=True)

    ordering = ['order']

    @property
    def absolute_url(self):
        try:
            return self.image.url
        except ValueError:
            return ''

    def get_filename(self):
        return os.path.basename(self.image.path)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('Picture')
        verbose_name_plural = _('Pictures')


class DealManager(models.Manager):
    def active(self, **kwargs):
        return self.filter(active=True, **kwargs)

    def on_sale(self, **kwargs):
        now = timezone.now()
        return self.active(start_date__lte=now, end_date__gte=now, **kwargs)


class Deal(models.Model):
    listing = models.ForeignKey(Listing, verbose_name=_('Listing'))
    price = MoneyField(_('Sale Price'), default=Money(0, USD), max_digits=12, decimal_places=2)
    active = models.BooleanField(_('Active'), default=False)
    start_date = models.DateTimeField(verbose_name=_('Activation date'))
    end_date = models.DateTimeField(verbose_name=_('Deactivation date'))

    objects = DealManager()

    def __unicode__(self):
        if self.listing.location is not None:
            return '%s - %s' % (self.listing.title, self.listing.location.name)
        return self.listing.title

    class Meta:
        verbose_name = _('Deal')
        verbose_name_plural = _('Deals')
