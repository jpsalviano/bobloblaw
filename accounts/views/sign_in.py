import json
import bcrypt

from django.http import JsonResponse
from django.views import View
from django.core import exceptions

from ..models import User
from ..forms import SignInForm


class SignIn(View):
    def post(self, request):
        try:
            form = SignInForm(json.loads(request.body))
            assert form.is_valid()
            user = User.objects.get(username=form.cleaned_data["username"])
            validate_password(form.cleaned_data["password"], user.password)
            response = JsonResponse({"username": user.username})
            response.status_code = 200
            return response
        except AssertionError:
            response = JsonResponse(form.errors)
            response.status_code = 400
            return response
        except User.DoesNotExist:
            response = JsonResponse({"username": ["Username does not exist."]})
            response.status_code = 401
            return response
        except ValidationError as error:
            response = JsonResponse({"password": ["Wrong password."]})
            response.status_code = 401
            return response


def validate_password(password_txt, password_hash):
    try:
        assert bcrypt.checkpw(password_txt, password_hash)
    except:
        raise exceptions.ValidationError("Wrong password.")
