import json
import jwt

from django.http import HttpResponse
from django.core.signing import Signer

from ..models import User

class AuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            access_token = json.loads(request.body.decode()).get("access_token")
            user_id = jwt.decode(access_token, Signer().sign("JWT"), algorithms=["HS256"]).get("sub")
            user = User.objects.get(id=user_id)
            request.user = user.id
            response = self.get_response(request)
        except User.DoesNotExist:
            request.user = None
            response = self.get_response(request)
        except jwt.exceptions.DecodeError:
            request.user = None
            response = self.get_response(request)
        except jwt.exceptions.ExpiredSignatureError:
            request.user = None
            response = self.get_response(request)
        except json.decoder.JSONDecodeError:
            request.user = None
            response = self.get_response(request)
        return response
