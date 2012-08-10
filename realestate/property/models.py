from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
from django.db import models
from django.contrib.auth.models import User
from sorl.thumbnail import ImageField

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

OFERTAS = ( ('venta', 'Venta'), ('alquiler', 'Alquiler'), ('venta_alquiler', 'Venta y/o Alquiler'))
ESTADO_PROPIEDAD = ( ('activa', 'Activa'), ('inactiva', 'Inactiva'), ('vendida', 'Vendida'))
ESTADO_ESPECIAL = ( ('activa', 'Activa'), ('inactiva', 'Inactiva'),)


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
    telefono = models.CharField(max_length=15)
    celular = models.CharField(max_length=15)
    ciudad = models.ForeignKey(Ciudad)
    direccion = models.CharField(max_length=200)
    user = models.OneToOneField(User)

    def __unicode__(self):
        if not self.user.first_name and not self.user.last_name:
            return self.user.username
        return self.user.first_name + " " + self.user.last_name

    class Meta:
        verbose_name = 'Agente'
        verbose_name_plural = 'Agentes'


class PropiedadManager(models.Manager):
    def activas(self, **kwargs):
        return self.filter(estado='activa', **kwargs)


class Propiedad(models.Model):
    titulo = models.CharField(max_length=60)
    slug = models.CharField(max_length=60, unique=True, blank=False)
    descripcion = models.TextField(max_length=1000)
    precio = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)
    sector = models.ForeignKey(Sector)
    tipo = models.CharField(max_length=30, choices=TIPO_PROPIEDADES)
    oferta = models.CharField(max_length=10, choices=OFERTAS)
    estado = models.CharField(max_length=10, choices=ESTADO_PROPIEDAD)
    agente = models.ForeignKey(Agente)
    creacion = models.DateTimeField(auto_now_add=True)
    niveles = models.IntegerField(max_length=2, default=1)
    dormitorios = models.IntegerField(max_length=2, default=3)
    banios = models.IntegerField(max_length=2, default=2)
    servicio = models.BooleanField(default=0)
    marquesina = models.IntegerField(max_length=2, default=0)
    tamano_solar = models.IntegerField(default=0)
    tamano_construccion = models.IntegerField(default=0)
    cocina = models.BooleanField(default=1)
    parqueo_techado = models.BooleanField(default=0)
    comedor = models.BooleanField(default=1)
    amueblado = models.BooleanField(default=0)
    piscina = models.BooleanField(default=0)
    balcon = models.IntegerField(max_length=2, default=0)
    intercom = models.BooleanField(default=0)
    notas = models.TextField(max_length=500)
    coordenadas = models.CharField(max_length=22, default='19.000000,-70.400000')
    featured = models.BooleanField(default=False)

    objects = PropiedadManager()

    def imagen_principal(self):
        im = self.imagen_propiedad_set.all()
        if im.count():
            return im[0]
        return None

    def get_address(self):
        return self.sector + ', ' + self.sector.ciudad + ', ' + self.sector.ciudad.provincia

    def __unicode__(self):
        return self.titulo

    class Meta:
        verbose_name = 'Propiedad'
        verbose_name_plural = 'Propiedades'

    def save(self, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titulo)
        super(Propiedad, self).save(**kwargs)


    def get_absolute_url(self):
        return reverse('property_details', args=[self.slug])


class Imagen_Propiedad(models.Model):
    titulo = models.CharField(max_length=60)
    imagen = ImageField(upload_to='propiedades/')
    propiedad = models.ForeignKey(Propiedad)
    agregada = models.DateTimeField(auto_now_add=True)
    orden = models.IntegerField(max_length=2, default=99, null=True)

    ordering = ['orden']

    def get_filename(self):
        return self.imagen.path.split('/')[-1]

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