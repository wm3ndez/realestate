from django.db import models
from django.utils.translation import ugettext_lazy as _


class Contact(models.Model):
    name = models.CharField(_('Name'), max_length=60)
    phone = models.CharField(_('Phone'), max_length=20, null=True, blank=True)
    cellphone = models.CharField(_('Cellphone'), max_length=20, null=True, blank=True)
    email = models.EmailField(_('Email'), null=True, blank=True)
    info = models.TextField(_('Info'), null=True, blank=True)
    date_added = models.DateTimeField(_('Date Added'), auto_now_add=True)

    class Meta:
        verbose_name = _('Contact')
        verbose_name_plural = _('Contacts')

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name
