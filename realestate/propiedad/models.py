# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
from django.db import models

from django.contrib.auth.models import User
import os
import re
from sorl.thumbnail import ImageField
from django.utils.translation import ugettext as _
from tinymce.models import HTMLField

TIPO_PROPIEDADES = (
    ('casa', 'Casas'),
    ('apartamento', 'Apartamentos'),
    ('local_comercial', 'Locales Comerciales'),
    ('solar', 'Solares'),
    ('penthouse', 'Penthouses'),
    ('oficina', 'Oficina'),
    ('finca', 'Finca'),
)
PROVINCIAS = (
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

OFERTAS = ( ('venta', 'Venta'), ('alquiler', 'Alquiler'), ('venta_alq', 'Venta y/o Alquiler'))
ESTADO_PROPIEDAD = ( ('activa', 'Activa'), ('inactiva', 'Inactiva'), ('vendida', 'Vendida'))
ESTADO_ESPECIAL = ( ('activa', 'Activa'), ('inactiva', 'Inactiva'),)

VALIDATIONS = [
    ('propiedad.utils.validation_simple', _('Uno o más caracteres')),
    ('propiedad.utils.validation_integer', _('Número entero')),
    ('propiedad.utils.validation_yesno', _('Si o No')),
    ('propiedad.utils.validation_decimal', _('Número decimal')),
]


class Ciudad(models.Model):
    nombre = models.CharField(max_length=45)
    provincia = models.CharField(max_length=45, choices=PROVINCIAS)

    def __unicode__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Ciudad'
        verbose_name_plural = 'Ciudades'


class Sector(models.Model):
    nombre = models.CharField(max_length=45)
    ciudad = models.ForeignKey(Ciudad)

    def __unicode__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Sector'
        verbose_name_plural = 'Sectores'


class Agente(models.Model):
    telefono = models.CharField(max_length=15, verbose_name=_(u'Teléfono'))
    celular = models.CharField(max_length=15, verbose_name=_(u'Celular'))
    ciudad = models.ForeignKey(Ciudad, verbose_name=_(u'Ciudad'))
    direccion = models.CharField(max_length=200, verbose_name=_(u'Dirección'))
    fotografia = ImageField(upload_to='agentes/', default='', verbose_name=_(u'Fotografía'))
    user = models.OneToOneField(User, verbose_name=_(u'Usuario'))

    def __unicode__(self):
        if (self.user.first_name or self.user.last_name):
            return '%s %s' % (self.user.first_name, self.user.last_name)
        return self.user.username

    class Meta:
        verbose_name = 'Agente'
        verbose_name_plural = 'Agentes'


class PropiedadManager(models.Manager):
    def activas(self, **kwargs):
        return self.filter(estado='activa', **kwargs)

    def casas(self, **kwargs):
        return self.activas().filter(tipo='casa')

    def apartamentos(self, **kwargs):
        return self.activas().filter(tipo='apartamento')

    def featured(self, **kwargs):
        return self.activas().filter(featured=True)

    def alquiler(self, **kwargs):
        return self.activas().filter(oferta__in=('venta_alq', 'alquiler'))

    def venta(self, **kwargs):
        return self.activas().filter(oferta__in=('venta_alq', 'venta'))


class Propiedad(models.Model):
    titulo = models.CharField(max_length=100, verbose_name=_(u'Título de la Propiedad'))
    slug = models.SlugField(max_length=100, unique=True, blank=False, verbose_name=_(u'Slug'))
    descripcion = HTMLField(max_length=1000, verbose_name=_(u'Descripción'))
    precio = models.FloatField(default=0.0, verbose_name=_(u'Precio'))
    sector = models.ForeignKey(Sector)
    tipo = models.CharField(max_length=30, choices=TIPO_PROPIEDADES, verbose_name=_(u'Tipo de Inmueble'))
    oferta = models.CharField(max_length=10, choices=OFERTAS, verbose_name=_(u'Oferta'))
    estado = models.CharField(max_length=10, choices=ESTADO_PROPIEDAD, verbose_name=_(u'Estado'))
    agente = models.ForeignKey(Agente)
    creacion = models.DateTimeField(auto_now_add=True, verbose_name=_(u'Creación'))
    niveles = models.IntegerField(max_length=2, default=1, verbose_name=_(u'Niveles'))
    dormitorios = models.IntegerField(max_length=2, default=3, verbose_name=_(u'Dormintorios'))
    banios = models.IntegerField(max_length=2, default=2, verbose_name=_(u'Baños'))
    servicio = models.BooleanField(default=0, verbose_name=_(u'Servicio?'))
    marquesina = models.IntegerField(max_length=2, default=0, verbose_name=_(u'Marquesina?'))
    tamano_solar = models.IntegerField(default=0, verbose_name=_(u'Área del Terreno'))
    tamano_construccion = models.IntegerField(default=0, verbose_name=_(u'Área de Construcción'))
    cocina = models.BooleanField(default=1, verbose_name=_(u'Cocina'))
    parqueo_techado = models.BooleanField(default=0, verbose_name=_(u'Parque Techado?'))
    comedor = models.BooleanField(default=1, verbose_name=_(u'Comedor?'))
    amueblado = models.BooleanField(default=0, verbose_name=_(u'Amueblado?'))
    piscina = models.BooleanField(default=0, verbose_name=_(u'Piscina?'))
    balcon = models.IntegerField(max_length=2, default=0, verbose_name=_(u'Balcón'))
    intercom = models.BooleanField(default=0, verbose_name=_(u'Intercom?'))
    notas = models.TextField(max_length=500, verbose_name=_(u'Notas privadas acerca de esta propiedad.'))
    coordenadas = models.CharField(max_length=22, default='19.000000,-70.400000', verbose_name=_(u'Coordenadas'))
    featured = models.BooleanField(default=False, verbose_name=_(u'Propiedad Destacada?'))
    vistas = models.IntegerField(verbose_name=_(u'Notas privadas acerca de esta propiedad.'), null=True)

    objects = PropiedadManager()

    def _imagen_principal(self):
        im = self.imagen_propiedad_set.all()
        if im.count():
            return im[0]
        return None

    imagen_principal = property(_imagen_principal)

    def get_address(self):
        return '%s, %s, %s' % (self.sector, self.sector.ciudad, self.sector.ciudad.provincia)

    def __unicode__(self):
        return self.titulo

    class Meta:
        verbose_name = 'Propiedad'
        verbose_name_plural = 'Propiedades'

    def save(self, **kwargs):
        self._generate_valid_slug()
        super(Propiedad, self).save(**kwargs)

    def _generate_valid_slug(self):
        if not self.is_valid_slug():
            slug = slugify(self.titulo)
            while Propiedad.objects.filter(slug=slug).exclude(id=self.id).exists():
                slug = '%s-1' % slug
            self.slug = slug

    def is_valid_slug(self):
        if self.slug is None or len(self.slug) < 10:
            return False
        match = re.match('[^\w\s-]', self.slug)
        if not match:
            return False
        return self.slug == slugify(self.slug)

    def get_absolute_url(self):
        return reverse('property_details', args=[self.slug])

    def get_features(self):
        features = [
            u'Niveles: %s' % self.niveles,
            u'Dormitorios: %s' % self.dormitorios,
            u'Baños: %s' % self.banios,
        ]
        if self.cocina:
            features.append(u'Cocina')
        if self.comedor:
            features.append(u'Comedor')
        if self.servicio:
            features.append(u'Hab. de Servicio')
        if self.amueblado:
            features.append(u'Amueblado/a')
        if self.piscina:
            features.append(u'Piscina')
        if self.balcon:
            features.append(u'%s balcon(es)' % self.balcon)
        if self.marquesina:
            features.append(u'Marquesina para %s vehículo(s)' % self.marquesina)
        if self.parqueo_techado:
            features.append(u'Parqueo Techado')
        if self.tamano_construccion:
            features.append(u'%s Mts2 de const.' % self.tamano_construccion)
        if self.tamano_solar:
            features.append(u'%s Mts2 de solar' % self.tamano_solar)

        return features

    def propiedades_en_el_area(self):
        return Propiedad.objects.filter(sector=self.sector).order_by('?')[:4]


class Atributos(models.Model):
    nombre = models.CharField(u'Atributo', max_length=100)
    validacion = models.CharField(u'Tipo de valor', choices=VALIDATIONS, max_length=100)

    class Meta:
        ordering = ('nombre',)
        verbose_name = 'Atributo'
        verbose_name_plural = 'Atributos'

    def __unicode__(self):
        return self.nombre


class AtributosPropiedad(models.Model):
    propiedad = models.ForeignKey(Propiedad)
    atributo = models.ForeignKey(Atributos)
    valor = models.CharField(u'Valor', max_length=255)

    class Meta:
        verbose_name = 'Atributo de Propiedad'
        verbose_name_plural = 'Atributos de Propiedad'

    def __unicode__(self):
        return self.atributo.nombre + ': ' + self.valor


class Imagen_Propiedad(models.Model):
    titulo = models.CharField(max_length=60)
    imagen = ImageField(upload_to='propiedades/')
    propiedad = models.ForeignKey(Propiedad)
    agregada = models.DateTimeField(auto_now_add=True)
    orden = models.IntegerField(max_length=2, default=99, null=True)

    ordering = ['orden']

    def get_filename(self):
        return os.path.basename(self.imagen.path)

    def __unicode__(self):
        return self.titulo

    class Meta:
        verbose_name = 'Fotografia'
        verbose_name_plural = 'Fotografias'


class Especial(models.Model):
    propiedad = models.ForeignKey(Propiedad)
    estado = models.CharField(choices=ESTADO_ESPECIAL, max_length=12)
    inicio = models.DateTimeField(verbose_name=u'Fecha de Activacion de la oferta')
    final = models.DateTimeField(verbose_name=u'Fecha de Desactivacion de la oferta')

    def __unicode__(self):
        return self.propiedad.titulo + ' - ' + self.propiedad.sector.nombre

    class Meta:
        verbose_name = 'Propiedad en Oferta'
        verbose_name_plural = 'Propiedades en Oferta'