from django.http import JsonResponse


def check_endpoint_status(request):
    response = JsonResponse({'endpoint status': 'ok'})
    response.status_code = 200
    return response
