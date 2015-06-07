from rest_framework import serializers

from realestate.listing.models import Listing


class ListingSerializer(serializers.Serializer):
    price = serializers.SerializerMethodField()
    currency = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()

    def get_images(self, listing):
        return listing.image_list

    def get_price(self, listing):
        return listing.price.amount

    def get_currency(self, listing):
        return listing.price.currency.code

    class Meta:
        model = Listing
        fields = ['id', 'title', 'description', 'absolute_url', 'price', 'currency', 'address', 'type', 'offer',
                  'active', 'baths', 'beds', 'size', 'coords', 'agent', 'created_at', 'last_modified', 'images', ]
