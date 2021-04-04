import json
import bcrypt

from django.http import HttpResponse, JsonResponse
from django.views import View
from django.core import exceptions

from ..auth_tools.auth_jwt import _generate_token
from ..models import User
from ..forms import SignInForm


class SignIn(View):
    def get(self, request):
        response = JsonResponse({"get signin form": "ok"})
        return response

    def post(self, request):
        try:
            form = SignInForm(json.loads(request.body.decode()))
            if not form.is_valid():
                response = JsonResponse(form.errors)
                response.status_code = 400
                return response
            user = User.objects.get(username=form.cleaned_data.get("username"))
            validate_password(form.cleaned_data.get("password"), user.password)
        except User.DoesNotExist:
            response = JsonResponse({"error": ["Username does not exist."]})
            response.status_code = 401
            return response
        except exceptions.ValidationError:
            response = JsonResponse({"error": ["Wrong password."]})
            response.status_code = 401
            return response
        else:
            response = HttpResponse()
            access_token = _generate_token(form.cleaned_data["username"])
            response["access_token"] = access_token
            response.status_code = 200
            return response


def validate_password(password_txt, password_hash):
    if not bcrypt.checkpw(password_txt.encode(), password_hash.encode()):
        raise exceptions.ValidationError("Wrong password.")
