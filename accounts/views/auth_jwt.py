import json
import jwt

from django.views import View
from django.http import JsonResponse
from django.core.signing import Signer


class GenerateToken(View):
    def post(self, request):
        user_id = json.loads(request.body)["user_id"]
        secret_key = Signer().sign("JWT")
        token = jwt.encode({"user_id": user_id}, secret_key, algorithm="HS256")
        return JsonResponse({"token": token})
