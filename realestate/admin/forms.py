from django import forms
from django.forms import ModelForm
from realestate.listing.models import Listing, Agent


class ListingForm(ModelForm):
    class Meta:
        model = Listing