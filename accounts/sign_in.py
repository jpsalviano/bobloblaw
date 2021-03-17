import json
import bcrypt
from secrets import token_hex

from django.http import JsonResponse
from django.views import View
from django.core import exceptions
from django.forms import ModelForm

from .models import User


class SignInForm(ModelForm):
    class Meta:
        model = User
        fields = ["username", "email"]
        

class SignIn(View):
    http_method_names = ['post']

    def post(self, request):
        try:
            user, password = self.validate_payload(json.loads(request.body))
            response = JsonResponse({"username": user.username})
            response.status_code = 200
            return response
        except User.DoesNotExist:
            response = JsonResponse({"error": "Username does not exist."})
            response.status_code = 403
            return response           
        except exceptions.ValidationError as error:
            response = JsonResponse({"error": error.message})
            response.status_code = 403
            return response

    def validate_payload(self, payload):
            username = payload["username"]
            user = User.objects.get(username=username)
            password = self.validate_password(payload, user)
            return user, password

    def validate_password(self, payload, user):
        password = payload["password"]
        if not bcrypt.checkpw(password.encode(), user.password.encode()):
            raise exceptions.ValidationError("Wrong password.")
        else:
            return password

    def validate_request(self, payload):
        password = self.validate_password(payload)
        username = self.validate_username(payload)
        email = self.validate_email(payload)
        return username, password, email
