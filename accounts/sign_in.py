import json
import bcrypt
from secrets import token_hex

from django.http import JsonResponse
from django.views import View
from django.core import exceptions

from .models import User, Session


class SignIn(View):
    http_method_names = ['post']

    def post(self, request):
        try:
            payload = json.loads(request.body)
            username = payload["username"]
            user = User.objects.get(username=username)
            password = self.validate_password(payload, user)
            session = Session.objects.create(user=user, session_token=token_hex(32))
            response = JsonResponse({"username": username, "session_token": session.session_token})
            response.status_code = 201
            return response
        except User.DoesNotExist:
            response = JsonResponse({"error": "Username does not exist."})
            response.status_code = 403
            return response           
        except exceptions.ValidationError as error:
            response = JsonResponse({"error": error.message})
            response.status_code = 403
            return response

    def validate_password(self, payload, user):
        password = payload["password"]
        if not bcrypt.checkpw(password.encode(), user.password.encode()):
            raise exceptions.ValidationError("Wrong password.")
        else:
            return password
