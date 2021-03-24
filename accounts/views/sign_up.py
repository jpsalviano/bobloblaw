import json
import os

from django.http import JsonResponse
from django.views import View
from django.core import exceptions
from django.conf import settings

from ..models import User
from ..forms import UserForm


class SignUp(View):
    def post(self, request):
        try:
            form = UserForm(json.loads(request.body))
            assert form.is_valid()
            form.save()
        except AssertionError:
            response = JsonResponse(form.errors)
            response.status_code = 400
            return response
        else:
            response = JsonResponse({"username": form.cleaned_data["username"]})
            response.status_code = 201
            return response
