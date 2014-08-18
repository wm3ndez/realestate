from django.conf import settings
from realestate.listing.models import OFFERS, TYPES, Agent, Location
from django import forms
from django.utils.translation import ugettext as _
from django.core.mail import send_mail, EmailMessage
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

    def send_contact_form(self, listing):
        asunto = '%s %s' % (_('Customer interested in:'), listing.title)
        # TODO: Translate
        message = "El cliente %s esta interesado en esta listing y le ha dejado el siguiente mensaje:\n\n%s\n\nTelefono: %s" % (
            self.cleaned_data.get('nombre'), self.cleaned_data.get('mensaje'), self.cleaned_data.get('phone'))
        _from = settings.DEFAULT_FROM_EMAIL
        to = [listing.agente.user.email, ]
        reply = self.cleaned_data.get('email')
        email = EmailMessage(asunto, message, _from, to, headers={'Reply-To': reply})
        email.send(fail_silently=False)


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

TIPO_PROPIEDADES_CHOICES = (('', _('All')),) + TYPES


class SearchForm(forms.Form):
    id = forms.CharField(required=False)
    agent = forms.ModelChoiceField(label=_('Agent'), queryset=Agent.objects.all(), required=False)
    location = forms.ModelChoiceField(label=_('Location'), queryset=Location.objects.states(), required=False)
    sector = forms.ModelChoiceField(label=_('Sector'), queryset=Location.objects.sectors(), required=False)
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