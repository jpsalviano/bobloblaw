from django.http import JsonResponse

from .sign_up import *
from .sign_in import *


def check_endpoint_status(request):
    response = JsonResponse({'status': 'ok'})
    response.status_code = 200
    return response
