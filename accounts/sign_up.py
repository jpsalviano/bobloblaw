import json
from secrets import token_hex

from django.http import JsonResponse
from django.views import View
from django.core import exceptions

from .models import User


class SignUp(View):
    def post(self, request):
        try:
            username, password, email = self.validate_payload(json.loads(request.body))
            user = User.objects.create(username=username, email=email, password=password)
            response = JsonResponse({"username": username, "email": email})
            response.status_code = 201
            return response
        except exceptions.ValidationError as error:
            response = JsonResponse({"error": error.message})
            response.status_code = 403
            return response
