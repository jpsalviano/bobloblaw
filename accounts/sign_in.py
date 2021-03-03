import json
import bcrypt
from secrets import token_hex

from django.http import JsonResponse
from django.views import View

from .models import User, Session


class SignIn(View):
    http_method_names = ['post']

    def post(self, request):
        try:
            create_session_data = json.loads(request.body)
            entered_password = create_session_data["password"]
            user = User.objects.get(username=create_session_data["username"])
            if bcrypt.checkpw(entered_password.encode(), user.password.encode()):
                session = Session.objects.create(user=user, session_token=token_hex(32))
                return JsonResponse({"logged": "true"})
            else:
                return JsonResponse({"error": "wrong password"})
        except Exception as e:
            return JsonResponse({"error": "undefined"})