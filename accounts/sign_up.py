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
            email = self.validate_email(payload)
            User.objects.create(username=username, email=email, password=password)
            response = JsonResponse({"username": username, "email": email})
            response.status_code = 201
            return response
        except exceptions.ValidationError as error:
            response = JsonResponse({"error": error.message})
            response.status_code = 403
            return response

    def validate_password(self, payload):
        try:
            password = payload["password"]
        except KeyError:
            raise exceptions.ValidationError("You must enter a password.")
        try:
            assert len(password) > 6
        except:
            raise exceptions.ValidationError("Password must be at least 7 characters long.")
        return password

    def validate_username(self, payload):
        username = payload["username"]
        if username:
            self.validate_username_length(username)
            self.validate_username_already_picked(username)
        else:
            raise exceptions.ValidationError("Username cannot be null.")
        return username

    def validate_username_length(self, username):
        if len(username) > 4:
            if len(username) > 20:
                raise exceptions.ValidationError("Username is too long.")
        else:
            raise exceptions.ValidationError("Username is too short.")

    def validate_username_already_picked(self, username):
        if User.objects.filter(username=username):
            raise exceptions.ValidationError("Username is already picked.")

    def validate_email(self, payload):
        email = payload["email"]
        if User.objects.filter(email=email):
            raise exceptions.ValidationError("Email is already in use.")
        return email
