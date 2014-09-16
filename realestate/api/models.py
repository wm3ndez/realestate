import binascii
from django.contrib.auth.models import User
import os
from django.db import models
from django.utils.translation import ugettext_lazy as _

from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class ApiKeys(models.Model):
    description = models.CharField(max_length=100, blank=True, default='', verbose_name=_('Description'))
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
