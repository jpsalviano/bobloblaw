import json
import bcrypt
from secrets import token_hex

from django.http import JsonResponse
from django.views import View
from django.core import exceptions
from django.forms import ModelForm

from .models import User


class SignInForm(ModelForm):
    """docstring for SignInForm"""
    def __init__(self, arg):
        super(SignInForm, self).__init__()
        self.arg = arg
        

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

    def validate_password(self, payload):
            try:
                password, password2 = payload["password"], payload["password2"]
            except:
                raise exceptions.ValidationError("You must enter the password twice.")
            try:
                assert password == password2
            except:
                raise exceptions.ValidationError("Passwords do not match.")
            try:
                assert len(password) > 6
            except:
                raise exceptions.ValidationError("Password must be at least 7 characters long.")
            return password

    def validate_username(self, payload):
        try:
            username = payload["username"]
        except KeyError:
            raise exceptions.ValidationError("You must enter a username.")
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
        try:
            email = payload["email"]
        except KeyError:
            raise exceptions.ValidationError("You must enter an email.")
        if User.objects.filter(email=email):
            raise exceptions.ValidationError("Email is already in use.")
        return email
