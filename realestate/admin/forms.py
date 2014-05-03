from django.forms import ModelForm
from realestate.listing.models import Listing, AttributeListing, ListingImage
from django.forms.models import inlineformset_factory


class ListingForm(ModelForm):
    class Meta:
        model = Listing

ListingImageFormSet = inlineformset_factory(Listing, ListingImage)
AttributeListingFormSet = inlineformset_factory(Listing, AttributeListing)