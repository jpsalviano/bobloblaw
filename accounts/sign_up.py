import json
import bcrypt

from django.http import JsonResponse

from .models import User


class SignUp:
    def sign_up(request):
        try:
            request.method == 'POST'
            user_signup_data = json.loads(request.body)
            encrypted_password = SignUp.encrypt_password(user_signup_data["password"])
            user = User.objects.create(username=user_signup_data["username"], email=user_signup_data["email"], password=encrypted_password)
            user.full_clean()
        except Exception as e:
            raise e
        else:
            user.save()
            response = JsonResponse({"user_created": "ok"})
            response.status_code = 201
            return response

    @classmethod
    def encrypt_password(cls, password):
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode(), salt)
        return hashed