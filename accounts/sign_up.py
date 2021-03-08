import json

from django.http import JsonResponse
from django.views import View
from django.core import exceptions

from .models import User


class SignUp(View):
    def post(self, request):
        try:
            payload = json.loads(request.body)
            password = self.validate_password(payload)
            username = self.validate_username(payload)
            User.objects.create(username=username, email=payload["email"], password=password)
            response = JsonResponse({"user_created": "ok"})
            response.status_code = 201
            return response
        except Exception as e:
            raise e

    def validate_password(self, payload):
        password1, password2 = payload["password1"], payload["password2"]
        if password1 == password2:
            return password1
        else:
            raise exceptions.ValidationError("Passwords do not match.")

    def validate_username(self, payload):
        username = payload["username"]
        try:
            len(username) > 4
        except:
            raise exceptions.ValidationError("Username is too short.")
        try:
            len(username) < 21
        except:
            raise exceptions.ValidationError("Username is too long.")
        return username