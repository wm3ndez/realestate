from rest_framework import viewsets
from realestate.propiedad.models import Propiedad


class PropiedadViewSet(viewsets.ModelViewSet):
    model = Propiedad