from django.template.defaultfilters import slugify
from realestate.listing.models import Listing, Sector, City, Agent, ListingImage
import os
from django.core.management.base import BaseCommand
from django.conf import settings
import csv


class Command(BaseCommand):
    def handle(self, *args, **options):
        reader = csv.reader(open(os.path.abspath(os.path.join(settings.PROJECT_ROOT, '../csv/propiedades.csv')), 'r'))
        for propiedad in reader:
            if propiedad[0] == 'title': continue

            titulo = propiedad[0]
            slug = slugify(titulo)
            try:
                prop = Listing.objects.get(slug=slug)
            except Listing.DoesNotExist:
                prop = Listing(titulo=titulo, slug=slug)
                prop.price = propiedad[1]
                prop.description = propiedad[2]
                try:
                    sector = Sector.objects.get(nombre=propiedad[3].capitalize())
                except Sector.DoesNotExist:
                    ciudad = City.objects.get_or_create(nombre='Santiago', provincia='Santiago')[0]
                    ciudad.save()
                    sector = Sector(nombre=propiedad[3].capitalize(), ciudad=ciudad)
                    sector.save()

                prop.sector = sector

                prop.offer = propiedad[4].lower()
                prop.type = propiedad[5].lower()

                agente = Agent.objects.get(user__username='holguin')
                prop.agent = agente
                prop.coords = '19.450927,-70.694743'
                prop.notes = ''
                prop.status = 'activa'
                prop.save()

            imagen = ListingImage(titulo='', propiedad=prop)
            imagen.image.name = 'propiedades/' + propiedad[6]
            if not os.path.isfile(imagen.image.path): continue
            if int(propiedad[7]):
                imagen.order = 0
            imagen.save()

            print prop