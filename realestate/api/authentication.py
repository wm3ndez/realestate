from django.contrib.auth.models import AnonymousUser
from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from realestate.api.models import ApiKeys
from django.utils.translation import ugettext as _


class ApiKeyAuthentication(BaseAuthentication):
    def authenticate(self, request):
        key = request.META.get('X-API-Key')
        if not key:
            return None

        try:
            api_key = ApiKeys.objects.get(key=key)
            user = AnonymousUser()
        except ApiKeys.DoesNotExist:
            raise exceptions.AuthenticationFailed(_('The API Key is not valid'))

        return user, None