from django import forms
from django.contrib.auth.models import User
from realestate.listing.models import Listing, AttributeListing, ListingImage
from django.forms.models import inlineformset_factory
from constance import config, settings
from constance.admin import FIELDS
from django.utils.translation import gettext_lazy as _


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
        exclude = ('slug',)


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        exclude = ('password', 'is_superuser', 'user_permissions', 'last_login', 'date_joined',)


class SetPasswordForm(forms.Form):
    new_password = forms.CharField(label=_('Password'), max_length=20, widget=forms.PasswordInput, required=True)
    new_password1 = forms.CharField(label=_('Password(again)'), max_length=20, widget=forms.PasswordInput,
                                    required=True)

    def clean(self):
        password = self.cleaned_data.get('new_password')
        password1 = self.cleaned_data.get('new_password1')

        if password and password != password1:
            raise forms.ValidationError(_("Passwords don't match"))

        return self.cleaned_data


ListingImageFormSet = inlineformset_factory(Listing, ListingImage, can_delete=True)
AttributeListingFormSet = inlineformset_factory(Listing, AttributeListing, can_delete=True)