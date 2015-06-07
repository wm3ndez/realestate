from rest_framework import viewsets
from realestate.listing.models import Listing
from realestate.api.serializers import ListingSerializer


class PaginationMixin(object):
    paginate_by = 15
    paginate_by_param = 'limit'
    max_paginate_by = 100


class ListingViewSet(PaginationMixin, viewsets.ReadOnlyModelViewSet):
    model = Listing
    serializer_class = ListingSerializer
    queryset = Listing.objects.none()

    def get_queryset(self):
        queryset = Listing.objects.active()

        last_modified = self.request.QUERY_PARAMS.get('modified_from')
        if last_modified is not None:
            queryset = queryset.filter(last_modified__gt=last_modified)

        return queryset
