from django.views import View
from django.http import JsonResponse
from django.utils.decorators import method_decorator

from ..auth_tools.auth_decorator import login_required

class Private(View):
    @login_required
    def get(self, request):
        response = JsonResponse({"private_endpoint": "ok"})
        return response

    @login_required
    def post(self, request):
        user = request.user
        response = JsonResponse({"username": user})
        return response
