from functools import wraps
from django.http import JsonResponse


def login_required(endpoint):
    @wraps(endpoint)
    def _wrapped_view(self, request, *args, **kwargs):
        if request.user != None:
            return endpoint(self, request, *args, **kwargs)
        else:
            response = JsonResponse({"error": ["Forbidden."]})
            response.status_code = 403
            return response
    return _wrapped_view
