import json

from django.http import JsonResponse

from .models import User


def check_endpoint_status(request):
    response = JsonResponse({'status': 'ok'})
    response.status_code = 200
    return response

def signup(request):
    request.method == 'POST'
    data = request.body.decode()
    response = JsonResponse({'data': data})
    return response