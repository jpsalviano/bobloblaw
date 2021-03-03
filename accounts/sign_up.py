import json

from django.http import JsonResponse
from django.views import View

from .models import User


class SignUp(View):
    def post(self, request):
        user_signup_data = json.loads(request.body)
        user = User.objects.create(username=user_signup_data["username"], email=user_signup_data["email"], password=user_signup_data["password"])
        response = JsonResponse({"user_created": "ok"})
        response.status_code = 201
        return response
