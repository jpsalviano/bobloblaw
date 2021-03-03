import json

from django.http import JsonResponse

from .models import User


class SignUp:
    def sign_up(request):
        try:
            request.method == 'POST'
            user_signup_data = json.loads(request.body)
            user = User.objects.create(username=user_signup_data["username"], email=user_signup_data["email"], password=user_signup_data["password"])
        except Exception as e:
            raise e
        else:
            user.save()
            response = JsonResponse({"user_created": "ok"})
            response.status_code = 201
            return response
