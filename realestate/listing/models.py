# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
from django.db import models
from django.utils import timezone
from djmoney.models.fields import MoneyField
from moneyed import USD, Money

from django.contrib.auth.models import User
import os
import re
from sorl.thumbnail import ImageField
from django.utils.translation import ugettext as _
from realestate.home.models import Contact

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

# TODO: Change this to states
DOMINICAN_PROVINCES = (
    ('Azua', 'Azua'),
    ('Bahoruco', 'Bahoruco'),
    ('Barahona', 'Barahona'),
    ('Bavaro', 'Bavaro'),
    ('Dajabon', 'Dajabon'),
    ('Duarte', 'Duarte'),
    ('El Seibo', 'El Seibo'),
    ('Elias Pina', 'Elias Pina'),
    ('Espaillat', 'Espaillat'),
    ('Gaspar Hernandez', 'Gaspar Hernandez'),
    ('Hato Mayor', 'Hato Mayor'),
    ('Independencia', 'Independencia'),
    ('La Altagracia', 'La Altagracia'),
    ('La Romana', 'La Romana'),
    ('La Vega', 'La Vega'),
    ('Maria Trinidad Sanchez', 'Maria Trinidad Sanchez'),
    ('Monsenor Nouel', 'Monsenor Nouel'),
    ('Monte Plata', 'Monte Plata'),
    ('Montecristi', 'Montecristi'),
    ('Nagua', 'Nagua'),
    ('Ocoa', 'Ocoa'),
    ('Pedernales', 'Pedernales'),
    ('Peravia', 'Peravia'),
    ('Puerto Plata', 'Puerto Plata'),
    ('Salcedo', 'Salcedo'),
    ('Samana', 'Samana'),
    ('San Cristobal', 'San Cristobal'),
    ('San Francisco de Macoris', 'San Francisco de Macoris'),
    ('San Juan', 'San Juan'),
    ('San Pedro De Macoris', 'San Pedro De Macoris'),
    ('Sanchez Ramirez', 'Sanchez Ramirez'),
    ('Santiago', 'Santiago'),
    ('Santiago Rodriguez', 'Santiago Rodriguez'),
    ('Santo Domingo', 'Santo Domingo'),
    ('Valverde', 'Valverde'),
)

OFFERS = (('buy', _('For Sale')), ('rent', _('For Rent')), ('buy-rent', _('For Sale/For Rent')))

VALIDATIONS = [
    ('realestate.listing.utils.validation_simple', _(u'One or more characters')),
    ('realestate.listing.utils.validation_integer', _(u'Integer')),
    ('realestate.listing.utils.validation_yesno', _(u'Yes/No')),
    ('realestate.listing.utils.validation_decimal', _(u'Decimal')),
]


class CityManager(models.Manager):
    def containing_properties(self, **kwargs):
        return self.filter(sector__listing__isnull=False, **kwargs).distinct()


class City(models.Model):
    name = models.CharField(max_length=45)
    province = models.CharField(max_length=45, choices=DOMINICAN_PROVINCES)

    objects = CityManager()

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('City')
        verbose_name_plural = _('Cities')


class SectorManager(models.Manager):
    def containing_properties(self, **kwargs):
        return self.filter(listing__isnull=False, **kwargs).distinct()


class Sector(models.Model):
    name = models.CharField(max_length=45)
    city = models.ForeignKey(City)

    objects = SectorManager()

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('Sector')
        verbose_name_plural = _('Sectors')


class AgentManager(models.Manager):
    def active(self, **kwargs):
        return self.filter(active=True, **kwargs)

    def with_listings(self, **kwargs):
        return self.active(listing__isnull=False, **kwargs)


class Agent(models.Model):
    phone = models.CharField(max_length=15, verbose_name=_(u'Phone'), null=True, blank=True)
    mobile = models.CharField(max_length=15, verbose_name=_(u'Cellphone'), null=True, blank=True)
    city = models.ForeignKey(City, verbose_name=_(u'City'), null=True, blank=True)
    direccion = models.CharField(max_length=200, verbose_name=_(u'Address'), null=True, blank=True)
    image = ImageField(upload_to='agentes/', default='', verbose_name=_(u'Picture'), null=True, blank=True)
    user = models.OneToOneField(User, verbose_name=_(u'User'))
    active = models.BooleanField(default=False, verbose_name=_('Active'))

    objects = AgentManager()

    @property
    def name(self):
        if (self.user.first_name or self.user.last_name):
            return '%s %s' % (self.user.first_name, self.user.last_name)
        return self.user.username

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
    title = models.CharField(max_length=100, verbose_name=_(u'Title'))
    slug = models.SlugField(max_length=100, unique=True, blank=False, verbose_name=_(u'Slug'))
    description = models.TextField(verbose_name=_(u'Description'), null=True, blank=True)
    price = MoneyField(default=Money(0, USD), max_digits=12, decimal_places=2, verbose_name=_(u'Price'))
    sector = models.ForeignKey(Sector, null=True, blank=True)
    type = models.CharField(_(u'Listing Type'), max_length=30, choices=TYPES)
    offer = models.CharField(max_length=10, choices=OFFERS, verbose_name=_(u'Offer'))
    active = models.BooleanField(_('Active'), default=False)
    featured = models.BooleanField(default=False, verbose_name=_(u'Featured'))
    baths = models.PositiveIntegerField(_(u'Bathrooms'), default=0, null=True, blank=True)
    beds = models.PositiveIntegerField(_(u'Bedrooms'), default=0, null=True, blank=True)
    size = models.PositiveIntegerField(_(u'Size(m2)'), default=0, null=True, blank=True)
    coords = models.CharField(max_length=255, default='19.000000,-70.400000', verbose_name=_(u'Coords'), null=True,
                              blank=True)
    agent = models.ForeignKey(Agent, null=True, blank=True, verbose_name=_('Agent'))
    contact = models.ForeignKey(Contact, null=True, blank=True)
    notes = models.TextField(max_length=500, verbose_name=_(u'Private Notes'), null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_(u'Created'))
    last_modified = models.DateTimeField(auto_now=True, verbose_name=_(u'Last Modified'))

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
        if self.sector is None:
            return _(u'No location provided')
        return '%s, %s, %s' % (self.sector, self.sector.city, self.sector.city.province)

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _(u'Listing')
        verbose_name_plural = _(u'Listings')
        ordering = ['-pk', ]

    def save(self, **kwargs):
        self._generate_valid_slug()
        super(Listing, self).save(**kwargs)

    def _generate_valid_slug(self):
        if not self.is_valid_slug():
            slug = slugify(self.title)
            while Listing.objects.filter(slug=slug).exclude(id=self.id).exists():
                slug = '%s-1' % slug
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
                attributes.append(u'%s: %s' % (attribute_name, attribute.value))
            elif attribute.attribute.validation == 'realestate.listing.utils.validation_yesno':
                attributes.append(u'%s' % attribute_name)
            else:
                if attribute.attribute.validation == 'realestate.listing.utils.validation_integer':
                    attributes.append(u'%s %s' % (attribute.value, attribute_name))
                else:
                    attributes.append(u'%.2f %s' % (attribute.value, attribute_name))

        return attributes

    def nearby(self):
        return Listing.objects.active(sector=self.sector).exclude(id=self.id).order_by('?')

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
        return OnSale.objects.on_sale(listing__in=(self,)).exists()


class Attribute(models.Model):
    name = models.CharField(_(u'Attribute'), max_length=100)
    validation = models.CharField(_(u'Value type'), choices=VALIDATIONS, max_length=100)

    class Meta:
        ordering = ('name',)
        verbose_name = _(u'Attribute')
        verbose_name_plural = _(u'Attributes')

    def __unicode__(self):
        return self.name


class AttributeListing(models.Model):
    listing = models.ForeignKey(Listing)
    attribute = models.ForeignKey(Attribute)
    value = models.CharField(_(u'Value'), max_length=255)
    # order = models.SmallIntegerField(u'Orden', default=99)

    class Meta:
        verbose_name = _(u'Listing attribute')
        verbose_name_plural = _(u'Listing attributes')
        # ordering = ['order', ]

    def __unicode__(self):
        return '%s: %s' % (self.attribute.name, self.value)


class ListingImage(models.Model):
    listing = models.ForeignKey(Listing, related_name='images', verbose_name=_('Listing'))
    name = models.CharField(_('Name'), max_length=60)
    image = ImageField(_('Image'), upload_to='listing/')
    added = models.DateTimeField(_('Added'), auto_now_add=True)
    order = models.IntegerField(_('Order'), max_length=2, default=99, null=True)

    ordering = ['order']

    @property
    def absolute_url(self):
        return self.image.url

    def get_filename(self):
        return os.path.basename(self.image.path)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('Picture')
        verbose_name_plural = _('Pictures')


class OnSaleManager(models.Manager):
    def active(self, **kwargs):
        return self.filter(active=True, **kwargs)

    def on_sale(self, **kwargs):
        now = timezone.now()
        return self.active(start_date__lte=now, end_date__gte=now, **kwargs)


class OnSale(models.Model):
    listing = models.ForeignKey(Listing, verbose_name=_('Listing'))
    price = MoneyField(_('Sale Price'), default=Money(0, USD), max_digits=12, decimal_places=2)
    active = models.BooleanField(_('Active'), default=False)
    start_date = models.DateTimeField(verbose_name=_(u'Activation date'))
    end_date = models.DateTimeField(verbose_name=_(u'Deactivation date'))

    objects = OnSaleManager()

    def __unicode__(self):
        if self.listing.sector is not None:
            return '%s - %s' % (self.listing.title, self.listing.sector.name)
        return self.listing.title

    class Meta:
        verbose_name = _(u'Deal')
        verbose_name_plural = _(u'Deals')
