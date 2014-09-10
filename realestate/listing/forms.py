from django.contrib.sites.models import Site
from django.conf import settings
from realestate.listing.models import TYPES
from django import forms
from django.utils.translation import ugettext as _
from django.core.mail import send_mail, EmailMessage
from constance import config


class ListingContactForm(forms.Form):
    name = forms.CharField(max_length=40, required=True)
    email = forms.EmailField(required=True)
    phone = forms.CharField(required=False)
    message = forms.CharField(widget=forms.Textarea)

    def clean(self):
        cleaned_data = super(ListingContactForm, self).clean()
        if not cleaned_data.get('message'):
            raise forms.ValidationError('El mensaje no puede estar en blanco.')
        return cleaned_data

    def send_contact_form(self, listing):
        subject = '%s %s' % (_('Customer interested in:'), listing.title)
        # TODO: Translate
        message = "El cliente %s esta interesado en esta listing y le ha dejado el siguiente mensaje:\n\n%s\n\nTelefono: %s" % (
            self.cleaned_data.get('name'), self.cleaned_data.get('message'), self.cleaned_data.get('phone'))
        _from = settings.DEFAULT_FROM_EMAIL
        to = [listing.agent.email, ]
        reply = self.cleaned_data.get('email')
        email = EmailMessage(subject, message, _from, to, headers={'Reply-To': reply})
        email.send(fail_silently=False)

        send_autoresponder(reply)


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

        send_autoresponder(from_name)


def send_autoresponder(recipient_email):
    from_email = config.CONTACT_DEFAULT_EMAIL
    from_name = '%s<%s>' % (Site.objects.first().name, from_email)
    subject = _('Contact Request')
    message = _("Thank you for contacting us.  We will contact you as soon as possible.")
    send_mail(subject, message, from_name, [recipient_email])