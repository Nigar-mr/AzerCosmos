from django.utils.translation import gettext_lazy as _
from django.conf import settings

from rest_framework import exceptions
from rest_framework.authentication import BasicAuthentication


class User:
    is_authenticated = True


class BasicAuthenticationNew(BasicAuthentication):

    def authenticate_credentials(self, userid, password, request=None):
        """
        Authenticate the userid and password against username and password
        with optional request for context.
        """
        if not hasattr(settings, "BASIC_AUTH"):
            raise exceptions.AuthenticationFailed(_('Invalid username/password.'))
        for obj in settings.BASIC_AUTH:
            if userid == obj["user"] and password == obj["pass"]:
                return (User, None)
        else:
            raise exceptions.AuthenticationFailed(_('Invalid username/password.'))
