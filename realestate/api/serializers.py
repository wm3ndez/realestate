from rest_framework import serializers
from django.forms import widgets


class ListingSerializer(serializers.Serializer):
    id = serializers.Field()
    title = serializers.CharField(required=False, max_length=100)
    description = serializers.CharField(widget=widgets.Textarea, max_length=1000)
    absolute_url = serializers.URLField(required=False)
    price = serializers.SerializerMethodField('get_price')
    currency = serializers.SerializerMethodField('get_currency')
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

    def get_images(self, listing):
        return listing.image_list

    def get_price(self, listing):
        return listing.price.amount

    def get_currency(self, listing):
        return listing.price.currency