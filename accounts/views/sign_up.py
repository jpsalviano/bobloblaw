import json
import os

from django.http import HttpResponse, JsonResponse
from django.views import View

from ..models import User
from ..forms import UserForm
from ..auth_tools.auth_jwt import _generate_token


class SignUp(View):
    def post(self, request):
        form = UserForm(json.loads(request.body.decode()))
        if form.is_valid():
            form.save()
        else:
            response = JsonResponse(form.errors)
            response.status_code = 400
            return response
        access_token = _generate_token(form.cleaned_data.get("username"))
        response = HttpResponse()
        response["access_token"] = access_token
        response.status_code = 201
        return response
