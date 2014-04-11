from django.template.defaultfilters import slugify
from realestate.propiedad.models import Propiedad, Sector, Ciudad, Agente, ImagenPropiedad
import os
from django.core.management.base import BaseCommand
from django.conf import settings
import csv


class Command(BaseCommand):
    def handle(self, *args, **options):
        reader = csv.reader(open(os.path.abspath(os.path.join(settings.PROJECT_ROOT, '../csv/propiedades.csv')), 'r'))
        for propiedad in reader:
            if propiedad[0] == 'titulo': continue

            titulo = propiedad[0]
            slug = slugify(titulo)
            try:
                prop = Propiedad.objects.get(slug=slug)
            except Propiedad.DoesNotExist:
                prop = Propiedad(titulo=titulo, slug=slug)
                prop.precio = propiedad[1]
                prop.descripcion = propiedad[2]
                try:
                    sector = Sector.objects.get(nombre=propiedad[3].capitalize())
                except Sector.DoesNotExist:
                    ciudad = Ciudad.objects.get_or_create(nombre='Santiago', provincia='Santiago')[0]
                    ciudad.save()
                    sector = Sector(nombre=propiedad[3].capitalize(), ciudad=ciudad)
                    sector.save()

                prop.sector = sector

                prop.oferta = propiedad[4].lower()
                prop.tipo = propiedad[5].lower()

                agente = Agente.objects.get(user__username='holguin')
                prop.agente = agente
                prop.coordenadas = '19.450927,-70.694743'
                prop.notas = ''
                prop.estado = 'activa'
                prop.save()

            imagen = ImagenPropiedad(titulo='', propiedad=prop)
            imagen.imagen.name = 'propiedades/' + propiedad[6]
            if not os.path.isfile(imagen.imagen.path): continue
            if int(propiedad[7]):
                imagen.orden = 0
            imagen.save()

            print prop