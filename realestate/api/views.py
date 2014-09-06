from rest_framework import viewsets
from realestate.listing.models import Listing
from realestate.api.serializers import ListingSerializer


class ListingViewSet(viewsets.ReadOnlyModelViewSet):
    model = Listing
    serializer_class = ListingSerializer

    def get_queryset(self):
        queryset = Listing.objects.active()

        last_modified = self.request.QUERY_PARAMS.get('modified_from')
        if last_modified is not None:
            queryset = queryset.filter(last_modified__gt=last_modified)

        return queryset
