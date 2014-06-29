from rest_framework import viewsets, serializers
from django.forms import widgets
from realestate.listing.models import Listing
from realestate.api.authentication import ApiKeyAuthentication


class PropertySerializer(serializers.Serializer):
    id = serializers.Field()
    title = serializers.CharField(required=False, max_length=100)
    description = serializers.CharField(widget=widgets.Textarea, max_length=1000)
    absolute_url = serializers.URLField(required=False)
    price = serializers.FloatField(required=False)
    address = serializers.CharField(required=False, max_length=255)
    type = serializers.CharField(required=False, max_length=30)
    offer = serializers.CharField(required=False, max_length=10)
    active = serializers.BooleanField(required=False)
    baths = serializers.IntegerField(required=False)
    beds = serializers.IntegerField(required=False)
    size = serializers.FloatField(required=False)
    coords = serializers.CharField(required=False, max_length=255)
    agent = serializers.CharField(required=False, max_length=100)
    created_at = serializers.CharField(required=False, max_length=100)
    last_modified = serializers.CharField(required=False, max_length=100)
    images = serializers.SerializerMethodField('get_images')

    def get_images(self, obj):
        return obj.image_list


class PropiedadViewSet(viewsets.ReadOnlyModelViewSet):
    model = Listing
    serializer_class = PropertySerializer

    def get_queryset(self):
        queryset = Listing.objects.all()

        last_modified = self.request.QUERY_PARAMS.get('modified_from')
        if last_modified is not None:
            queryset = queryset.filter(last_modified__gt=last_modified)

        return queryset