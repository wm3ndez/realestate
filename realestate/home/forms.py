from realestate.listing.models import DOMINICAN_PROVINCES, OFFERS, TYPES, Agent, Sector
from django import forms
from django.utils.translation import ugettext as _

BATHROOMS_RANGE = (
    ('', '--'),
    ('1', '1+'),
    ('2', '2+'),
    ('3', '3+'),
    ('4', '4+'),
    ('5', '5+'),
    ('6', '6+'),
    ('7', '7+'),
    ('8', '8+'),
    ('9', '9+'),
    ('10', '10+'),
)

BEDROOMS_RANGE = (
    ('', '--'),
    ('1', '1+'),
    ('2', '2+'),
    ('3', '3+'),
    ('4', '4+'),
    ('5', '5+'),
    ('6', '6+'),
    ('7', '7+'),
    ('8', '8+'),
    ('9', '9+'),
    ('10', '10+'),
)

PROVINCIAS_CHOICES = (('', _('All')),) + DOMINICAN_PROVINCES
TIPO_PROPIEDADES_CHOICES = (('', _('All')),) + TYPES


class SearchForm(forms.Form):
    id = forms.CharField(required=False)
    agente = forms.ModelChoiceField(label=_('Agent'), queryset=Agent.objects.all(), required=False)
    location = forms.ChoiceField(label=_('Location'), choices=PROVINCIAS_CHOICES, required=False)
    sector = forms.ModelChoiceField(label=_('Sector'), queryset=Sector.objects.containing_properties(), required=False)
    tipo = forms.ChoiceField(label=_('Type'), choices=TIPO_PROPIEDADES_CHOICES, required=False)
    oferta = forms.ChoiceField(label=_('Offer'), choices=OFFERS, required=False)
    beds = forms.ChoiceField(label=_('Bedrooms'), choices=BEDROOMS_RANGE, required=False)
    baths = forms.ChoiceField(label=_('Bathrooms'), choices=BATHROOMS_RANGE, required=False)


class ContactForm(forms.Form):
    subject = forms.CharField(max_length=60, required=True)
    email = forms.EmailField(required=True)
    message = forms.CharField(widget=forms.Textarea)