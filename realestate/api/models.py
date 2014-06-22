import binascii
import os
from django.db import models
from django.utils.translation import ugettext as _


class ApiKeys(models.Model):
    key = models.CharField(max_length=40, primary_key=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('API Key')
        verbose_name_plural = _('API Keys')

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super(ApiKeys, self).save(*args, **kwargs)

    def generate_key(self):
        return binascii.hexlify(os.urandom(20))

    def __unicode__(self):
        return self.key
