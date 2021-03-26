import json
import jwt

from django.http import HttpResponse
from django.core.signing import Signer

from ..models import User

class AuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if request.path == "/accounts/signin/" or request.path == "/accounts/signup/":
            return self.get_response(request)

        try:
            access_token = request.headers.get("access_token")
            user_id = jwt.decode(access_token, Signer().sign("JWT"), algorithms=["HS256"]).get("sub")
            user = User.objects.get(id=user_id)
        except jwt.exceptions.DecodeError:
            response = HttpResponse()
            response.status_code = 401
        else:
            if user:
                response = self.get_response(request)
            else:
                response = HttpResponse()
                response.status_code = 401
        return response
