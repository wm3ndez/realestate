from django.forms import ModelForm
from realestate.listing.models import Listing


class ListingForm(ModelForm):
    class Meta:
        model = Listing