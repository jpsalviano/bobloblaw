from django.http import JsonResponse


def login_required(endpoint, *args, **kwargs):
    user = kwargs.get("user")
    if user != None:
        return endpoint
    else:
        response = JsonResponse({"error": ["Forbidden."]})
        response.status_code = 403
        return response
