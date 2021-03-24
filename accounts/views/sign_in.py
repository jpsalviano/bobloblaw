import json
import bcrypt

from django.http import JsonResponse
from django.views import View
from django.core import exceptions

from ..models import User
from ..forms import SignInForm
from .auth_jwt import _generate_token


class SignIn(View):
    def post(self, request):
        try:
            form = SignInForm(json.loads(request.body))
            assert form.is_valid()
            user = User.objects.get(username=form.cleaned_data["username"])
            validate_password(form.cleaned_data["password"], user.password)

        except AssertionError:
            response = JsonResponse(form.errors)
            response.status_code = 400
            return response
        except User.DoesNotExist:
            response = JsonResponse({"error": ["Username does not exist."]})
            response.status_code = 401
            return response
        except exceptions.ValidationError as error:
            response = JsonResponse({"error": ["Wrong password."]})
            response.status_code = 401
            return response
        else:
            access_token = _generate_token(form.cleaned_data["username"])
            response = JsonResponse({"access_token": access_token})
            response.status_code = 200
            return response


def validate_password(password_txt, password_hash):
    try:
        assert bcrypt.checkpw(password_txt.encode(), password_hash.encode())
    except:
        raise exceptions.ValidationError("Wrong password.")
