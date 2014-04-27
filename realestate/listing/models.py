# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
from django.db import models
from djmoney.models.fields import MoneyField
from moneyed import USD, Money

from django.contrib.auth.models import User
import os
import re
from sorl.thumbnail import ImageField
from django.utils.translation import ugettext as _
from realestate.home.models import Contacto

TYPES = (
    ('casa', 'Casas'),
    ('apartamento', 'Apartamentos'),
    ('local_comercial', 'Locales Comerciales'),
    ('solar', 'Solares'),
    ('penthouse', 'Penthouses'),
    ('oficina', 'Oficina'),
    ('finca', 'Finca'),
)
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

OFFERS = (('venta', 'Venta'), ('alquiler', 'Alquiler'), ('venta_alq', 'Venta y/o Alquiler'))
LISTING_STATUS = (('activa', 'Activa'), ('inactiva', 'Inactiva'), ('vendida', 'Vendida'))
SALE_STATUS = (('activa', 'Activa'), ('inactiva', 'Inactiva'),)

VALIDATIONS = [
    ('realestate.listing.utils.validation_simple', _(u'Uno o más caracteres')),
    ('realestate.listing.utils.validation_integer', _(u'Número entero')),
    ('realestate.listing.utils.validation_yesno', _(u'Si o No')),
    ('realestate.listing.utils.validation_decimal', _(u'Número decimal')),
]


class CityManager(models.Manager):
    def containing_properties(self, **kwargs):
        return self.filter(sector__listing__isnull=False, **kwargs)


class City(models.Model):
    name = models.CharField(max_length=45)
    province = models.CharField(max_length=45, choices=DOMINICAN_PROVINCES)

    objects = CityManager()

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'City'
        verbose_name_plural = 'Ciudades'


class SectorManager(models.Manager):
    def containing_properties(self, **kwargs):
        return self.filter(listing__isnull=False, **kwargs)


class Sector(models.Model):
    name = models.CharField(max_length=45)
    city = models.ForeignKey(City)

    objects = SectorManager()

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'Sector'
        verbose_name_plural = 'Sectores'


class AgentManager(models.Manager):
    def active(self, **kwargs):
        return self.filter(active=True, **kwargs)

    def with_listings(self, **kwargs):
        return self.active(listing__isnull=False, **kwargs)


class Agent(models.Model):
    phone = models.CharField(max_length=15, verbose_name=_(u'Teléfono'), null=True, blank=True)
    mobile = models.CharField(max_length=15, verbose_name=_(u'Celular'), null=True, blank=True)
    city = models.ForeignKey(City, verbose_name=_(u'City'), null=True, blank=True)
    direccion = models.CharField(max_length=200, verbose_name=_(u'Dirección'), null=True, blank=True)
    image = ImageField(upload_to='agentes/', default='', verbose_name=_(u'Fotografía'), null=True, blank=True)
    user = models.OneToOneField(User, verbose_name=_(u'Usuario'))
    active = models.BooleanField(default=False, verbose_name=_('Activo'))

    objects = AgentManager()

    @property
    def name(self):
        if (self.user.first_name or self.user.last_name):
            return '%s %s' % (self.user.first_name, self.user.last_name)
        return self.user.username

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'Agente'
        verbose_name_plural = 'Agentes'


class ListingManager(models.Manager):
    def active(self, **kwargs):
        return self.filter(status='activa', **kwargs)

    def casas(self, **kwargs):
        return self.active().filter(type='casa')

    def apartamentos(self, **kwargs):
        return self.active().filter(type='apartamento')

    def featured(self, **kwargs):
        return self.active().filter(featured=True)

    def rent(self, **kwargs):
        return self.active().filter(offer__in=('venta_alq', 'alquiler'))

    def sale(self, **kwargs):
        return self.active().filter(offer__in=('venta_alq', 'venta'))


class Listing(models.Model):
    title = models.CharField(max_length=100, verbose_name=_(u'Título de la Propiedad'))
    slug = models.SlugField(max_length=100, unique=True, blank=False, verbose_name=_(u'Slug'))
    description = models.TextField(verbose_name=_(u'Descripción'), null=True, blank=True)
    price = MoneyField(default=Money(0, USD), max_digits=12, decimal_places=2, verbose_name=_(u'Precio'))
    sector = models.ForeignKey(Sector, null=True, blank=True)
    type = models.CharField(max_length=30, choices=TYPES, verbose_name=_(u'Tipo de Inmueble'))
    offer = models.CharField(max_length=10, choices=OFFERS, verbose_name=_(u'Oferta'))
    status = models.CharField(max_length=10, choices=LISTING_STATUS, verbose_name=_(u'Estado'))
    featured = models.BooleanField(default=False, verbose_name=_(u'Propiedad Destacada?'))
    frontpage = models.BooleanField(default=False, verbose_name=_(u'Mostrar en Frontpage?'))
    baths = models.PositiveIntegerField(_(u'Baños'), default=0, null=True, blank=True)
    beds = models.PositiveIntegerField(_(u'Dormitorios'), default=0, null=True, blank=True)
    size = models.PositiveIntegerField(_(u'Metros cuadrados(m2)'), default=0, null=True, blank=True)
    coords = models.CharField(max_length=255, default='19.000000,-70.400000', verbose_name=_(u'Coordenadas'), null=True,
                              blank=True)
    agent = models.ForeignKey(Agent, null=True, blank=True)
    contact = models.ForeignKey(Contacto, null=True, blank=True)
    notes = models.TextField(max_length=500, verbose_name=_(u'Notas privadas.'), null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_(u'Creación'))
    last_modified = models.DateTimeField(auto_now=True, verbose_name=_(u'Última Modificación'))

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
            return u'Ubicación no provista'
        return '%s, %s, %s' % (self.sector, self.sector.city, self.sector.city.province)

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = 'Propiedad'
        verbose_name_plural = 'Propiedades'

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
            if attribute.attribute.validation == 'realestate.listing.utils.validation_simple':
                attributes.append(u'%s: %s' % (attribute.attribute.nombre, attribute.value))
            elif attribute.attribute.validation == 'realestate.listing.utils.validation_yesno':
                attributes.append(u'%s' % attribute.value)
            else:
                if attribute.attribute.validation == 'realestate.listing.utils.validation_integer':
                    attributes.append(u'%s %s' % (attribute.value, attribute.attribute.nombre))
                else:
                    attributes.append(u'%.2f %s' % (attribute.value, attribute.attribute.nombre))

        return attributes

    def nearby(self):
        return Listing.objects.filter(sector=self.sector).order_by('?')[:4]


class Attribute(models.Model):
    name = models.CharField(u'Atributo', max_length=100)
    validation = models.CharField(u'Tipo de valor', choices=VALIDATIONS, max_length=100)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Atributo'
        verbose_name_plural = 'Atributos'

    def __unicode__(self):
        return self.name


class AttributeListing(models.Model):
    listing = models.ForeignKey(Listing)
    attribute = models.ForeignKey(Attribute)
    value = models.CharField(u'Valor', max_length=255)
    # order = models.SmallIntegerField(u'Orden', default=99)

    class Meta:
        verbose_name = 'Atributo de Propiedad'
        verbose_name_plural = 'Atributos de Propiedad'
        # ordering = ['order', ]

    def __unicode__(self):
        return '%s: %s' % (self.attribute.name, self.value)


class ListingImage(models.Model):
    listing = models.ForeignKey(Listing, related_name='images')
    name = models.CharField(max_length=60)
    image = ImageField(upload_to='propiedades/')
    added = models.DateTimeField(auto_now_add=True)
    order = models.IntegerField(max_length=2, default=99, null=True)

    ordering = ['order']

    @property
    def absolute_url(self):
        return self.image.url

    def get_filename(self):
        return os.path.basename(self.image.path)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'Fotografia'
        verbose_name_plural = 'Fotografias'


class OnSale(models.Model):
    listing = models.ForeignKey(Listing)
    status = models.CharField(choices=SALE_STATUS, max_length=12)
    start_date = models.DateTimeField(verbose_name=u'Fecha de Activacion de la offer')
    end_date = models.DateTimeField(verbose_name=u'Fecha de Desactivacion de la offer')

    def __unicode__(self):
        return '%s - %s' % (self.listing.title, self.listing.sector.name)

    class Meta:
        verbose_name = 'Propiedad en Oferta'
        verbose_name_plural = 'Propiedades en Oferta'
