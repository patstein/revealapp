from django.contrib.auth.models import AnonymousUser

from rest_framework.request import Request
from rest_framework_jwt.authentication import JSONWebTokenAuthentication


class JWTAuthenticationMiddleware(object):
    """ Middleware for authenticating JSON Web Tokens in Authorize Header """

    def __init__(self, get_response):
        self.get_response = get_response

    @staticmethod
    def get_user_jwt(request):
        """
        Replacement for django session auth get_user & auth.get_user for
        JSON Web Token authentication. Inspects the token for the user_id,
        attempts to get that user from the DB & assigns the user on the
        request object. Otherwise it defaults to AnonymousUser.
        This will work with existing decorators like LoginRequired, whereas
        the standard restframework_jwt auth only works at the view level
        forcing all authenticated users to appear as AnonymousUser ;)
        Returns: instance of user object or AnonymousUser object
        """
        user = None
        try:
            user_jwt = JSONWebTokenAuthentication().authenticate(Request(request))
            if user_jwt is not None:
                # store the first part from the tuple (user, obj)
                user = user_jwt[0]
        except:  # noqa
            pass

        return user or AnonymousUser()

    def __call__(self, request):
        if not request.user.is_authenticated:
            request.user = self.get_user_jwt(request)
        response = self.get_response(request)
        return response
