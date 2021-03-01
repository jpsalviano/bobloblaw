import json

from django.http import JsonResponse

from .models import User


class SignUp:
    def sign_up(request):
        if request.method == 'POST':
            data = json.loads(request.body.decode())
            user = User.create_user(username=data['username'], email=data['email'], password=data['password'])
            response = validate_sign_up_info(user)
        else:
            response = JsonResponse({'error': 'unauthorized'})
            response.status_code = 401
        return response


    def validate_sign_up_info(user):
        try:
            user.full_clean()
            user.save()
            response = JsonResponse({'user_created': 'ok'})
            response.status_code = 201
            return response
        except Exception as error:
            response = JsonResponse({'error': error.messages[0]})
            response.status_code = 400
            return response
