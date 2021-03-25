import json

from ..models import User


def auth_middleware(get_response):
    # One-time configuration and initialization.

    def middleware(request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        # Check in request if there is an access_token set.
        try:
            access_token = request.headers["access_token"]
            assert access_token is True
            request.logged = True
            response = get_response(request)
        except AssertionError:
            request.logged = False
            response = get_response(request)
        except KeyError:
            request.logged = False
            response = get_response(request)

        # Code to be executed for each request/response after
        # the view is called.
        # Nothing.

        return response

    return middleware
