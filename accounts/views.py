import json

from django.http import JsonResponse

from .models import User


def check_endpoint_status(request):
    response = JsonResponse({'status': 'ok'})
    response.status_code = 200
    return response


def signup(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode())
        user = User.create_user(username=data['username'], email=data['email'], password=data['password'])
        user.save()
        return JsonResponse({'user_created': 'ok'})
    else:
        response = JsonResponse({'error': 'unauthorized'})
        response.status_code = 401
        return response