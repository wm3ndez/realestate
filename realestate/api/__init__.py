from rest_framework import viewsets, serializers
from django.forms import widgets
from realestate.propiedad.models import Propiedad, ImagenPropiedad


class PropertySerializer(serializers.Serializer):
    pk = serializers.Field()
    titulo = serializers.CharField(required=False, max_length=100)
    descripcion = serializers.CharField(widget=widgets.Textarea, max_length=1000)
    absolute_url = serializers.URLField(required=False)
    precio = serializers.FloatField(required=False)
    address = serializers.CharField(required=False, max_length=255)
    tipo = serializers.CharField(required=False, max_length=30)
    oferta = serializers.CharField(required=False, max_length=10)
    estado = serializers.CharField(required=False, max_length=10)
    banos = serializers.IntegerField(required=False)
    dormitorios = serializers.IntegerField(required=False)
    tamano = serializers.FloatField(required=False)
    coordenadas = serializers.CharField(required=False, max_length=255)
    agente = serializers.CharField(required=False, max_length=100)
    creacion = serializers.CharField(required=False, max_length=100)
    ultima_modificacion = serializers.CharField(required=False, max_length=100)
    images = serializers.SerializerMethodField('get_images')

    def get_images(self, obj):
        return obj.image_list


class PropiedadViewSet(viewsets.ReadOnlyModelViewSet):
    model = Propiedad
    serializer_class = PropertySerializer