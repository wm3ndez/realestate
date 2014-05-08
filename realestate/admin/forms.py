from django import forms
from realestate.listing.models import Listing, AttributeListing, ListingImage
from django.forms.models import inlineformset_factory
from constance import config, settings
from constance.admin import FIELDS


class ConstanceForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(ConstanceForm, self).__init__(*args, **kwargs)
        for name, (default, help_text) in settings.CONFIG.items():
            default = getattr(config, name, default)
            field_class, kwargs = FIELDS[type(default)]
            self.fields[name] = field_class(label=help_text, initial=default, **kwargs)

    def save(self):
        for name in self.cleaned_data:
            setattr(config, name, self.cleaned_data[name])


class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing


ListingImageFormSet = inlineformset_factory(Listing, ListingImage, can_delete=True)
AttributeListingFormSet = inlineformset_factory(Listing, AttributeListing, can_delete=True)