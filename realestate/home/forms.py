from realestate.listing.models import DOMINICAN_PROVINCES, OFFERS, TYPES, Agent, Sector
from django import forms

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

PROVINCIAS_CHOICES = (('', 'Todas'),) + DOMINICAN_PROVINCES
TIPO_PROPIEDADES_CHOICES = (('', 'Todos'),) + TYPES


class SearchForm(forms.Form):
    id = forms.CharField(required=False)
    agente = forms.ModelChoiceField(queryset=Agent.objects.all(), required=False)
    location = forms.ChoiceField(choices=PROVINCIAS_CHOICES, required=False)
    sector = forms.ModelChoiceField(queryset=Sector.objects.containing_properties(), required=False)
    tipo = forms.ChoiceField(choices=TIPO_PROPIEDADES_CHOICES, required=False)
    oferta = forms.ChoiceField(choices=OFFERS, required=False)
    beds = forms.ChoiceField(choices=BEDROOMS_RANGE, required=False)
    baths = forms.ChoiceField(choices=BATHROOMS_RANGE, required=False)


class ContactForm(forms.Form):
    subject = forms.CharField(max_length=60, required=True)
    email = forms.EmailField(required=True)
    message = forms.CharField(widget=forms.Textarea)