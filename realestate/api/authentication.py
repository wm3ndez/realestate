from django.contrib.auth.models import AnonymousUser
from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from realestate.api.models import ApiKeys
from django.utils.translation import ugettext as _


class ApiKeyAuthentication(BaseAuthentication):
    def authenticate(self, request):
        key = request.META.get('HTTP_X_API_KEY')
        if not key:
            raise exceptions.AuthenticationFailed(_('The API Key is missing'))

        try:
            api_key = ApiKeys.objects.get(key=key)
            user = AnonymousUser()
        except ApiKeys.DoesNotExist:
            raise exceptions.AuthenticationFailed(_('The API Key is not valid'))

        return user, None