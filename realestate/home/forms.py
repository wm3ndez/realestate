from realestate.property.models import PROVINCIAS, OFERTAS, TIPO_PROPIEDADES, Agente
from django import forms

PRICE_RANGE = (
    ('', '--'),
    (5000, '5,000'),
    (10000, '10,000'),
    (50000, '50,000'),
    (100000, '100,000'),
    (500000, '500,000'),
    (1000000, '1,000,000'),
    (5000000, '5,000,000'),
    (10000000, '10,000,000'),
    )

BATHROOMS_RANGE = (
    ('', '--'),
    ('1', '1+'),
    ('2', '2+'),
    ('3', '3+'),
    ('4', '4+'),
    ('5', '5+'),
    )

BEDROOMS_RANGE = (
    ('', '--'),
    ('1', '1+'),
    ('2', '2+'),
    ('3', '3+'),
    ('4', '4+'),
    ('5', '5+'),
    )

class SearchForm(forms.Form):
    location = forms.CharField(required=False)
    tipo = forms.ChoiceField(choices=TIPO_PROPIEDADES, required=False)
    precio_min = forms.ChoiceField(choices=PRICE_RANGE, required=False)
    precio_max = forms.ChoiceField(choices=PRICE_RANGE, required=False)
    oferta = forms.ChoiceField(choices=OFERTAS, required=False)
    beds = forms.ChoiceField(choices=BEDROOMS_RANGE, required=False)
    baths = forms.ChoiceField(choices=BATHROOMS_RANGE, required=False)


class ContactForm(forms.Form):
    subject = forms.CharField(max_length=60, required=True)
    email = forms.EmailField(required=True)
    message = forms.CharField(widget=forms.Textarea)
