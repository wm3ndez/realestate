from realestate.property.models import PROVINCIAS, OFERTAS, TIPO_PROPIEDADES, Agente
from django import forms

PRICE_RANGE = (
    ('', ''),
    (0, 0),
    (5000, 5000),
    (10000, 10000),
    (50000, 50000),
    (100000, 100000),
    (500000, 500000),
    (1000000, 1000000),
    (5000000, 5000000),
    (10000000, 10000000),
    )

class SearchForm(forms.Form):
    id = forms.IntegerField()
    titulo = forms.CharField()
    #agente = forms.ChoiceField(choices=Agente.objects.all())
    agente = forms.CharField()
    provincia = forms.ChoiceField(choices=PROVINCIAS)
    tipo = forms.ChoiceField(choices=TIPO_PROPIEDADES)
    precio_min = forms.ChoiceField(choices=PRICE_RANGE)
    precio_max = forms.ChoiceField(choices=PRICE_RANGE)
    oferta = forms.ChoiceField(choices=OFERTAS)


class ContactForm(forms.Form):
    subject = forms.CharField(max_length=60, required=True)
    email = forms.EmailField(required=True)
    message = forms.CharField(widget=forms.Textarea)
