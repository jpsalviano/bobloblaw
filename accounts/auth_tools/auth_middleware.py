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
            access_token = json.loads(request.body.decode()).get("access_token")
            user_id = jwt.decode(access_token, Signer().sign("JWT"), algorithms=["HS256"]).get("sub")
            user = User.objects.get(id=user_id)
            request.user = user.id
            response = self.get_response(request)
        except (jwt.exceptions.DecodeError, json.decoder.JSONDecodeError, User.DoesNotExist):
            response = HttpResponse()
            response.status_code = 401
        return response
