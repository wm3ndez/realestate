from realestate.listing.models import DOMINICAN_PROVINCES, OFFERS, TYPES, Agent, Sector
from django import forms
from django.utils.translation import ugettext as _
from django.conf import settings
from django.core.mail import send_mail
from constance import config


class ListingContactForm(forms.Form):
    nombre = forms.CharField(max_length=40, required=True)
    email = forms.EmailField(required=True)
    telefono = forms.CharField(required=False)
    mensaje = forms.CharField(widget=forms.Textarea)

    def clean(self):
        cleaned_data = super(ListingContactForm, self).clean()
        if not cleaned_data.get('mensaje'):
            raise forms.ValidationError('El mensaje no puede estar en blanco.')
        return cleaned_data


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
    agent = forms.ModelChoiceField(label=_('Agent'), queryset=Agent.objects.all(), required=False)
    location = forms.ChoiceField(label=_('Location'), choices=PROVINCIAS_CHOICES, required=False)
    sector = forms.ModelChoiceField(label=_('Sector'), queryset=Sector.objects.containing_properties(), required=False)
    type = forms.ChoiceField(label=_('Type'), choices=TIPO_PROPIEDADES_CHOICES, required=False)
    offer = forms.ChoiceField(label=_('Offer'), choices=OFFERS, required=False)
    beds = forms.ChoiceField(label=_('Bedrooms'), choices=BEDROOMS_RANGE, required=False)
    baths = forms.ChoiceField(label=_('Bathrooms'), choices=BATHROOMS_RANGE, required=False)


class ContactForm(forms.Form):
    name = forms.CharField(label=_('Name'), max_length=60, required=True)
    subject = forms.CharField(label=_('Subject'), max_length=60, required=True)
    email = forms.EmailField(label=_('Email'), required=True)
    message = forms.CharField(label=_('Message'), widget=forms.Textarea, required=True)

    recipient_list = [config.CONTACT_DEFAULT_EMAIL]

    def send_email(self):
        from_email = self.cleaned_data['email']
        from_name = '%s<%s>' % (self.cleaned_data['name'], from_email)
        subject = self.cleaned_data['subject']
        message = self.cleaned_data['message']
        send_mail(subject, message, from_name, self.recipient_list)