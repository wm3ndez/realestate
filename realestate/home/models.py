from django.db import models
from django.utils.translation import ugettext as _


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


class Links(models.Model):
    name = models.CharField(max_length=32)
    link = models.URLField(max_length=255)
    description = models.CharField(max_length=150)
    contact = models.OneToOneField(Contact)
    active = models.BooleanField(default=False)

    def get_url(self):
        if self.link.startswith('http'):
            return self.link
        return 'http://%s' % self.link

    class Meta:
        verbose_name = 'Link'
        verbose_name_plural = 'Links'

    def __unicode__(self):
        return self.name
