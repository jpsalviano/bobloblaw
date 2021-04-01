from django.views import View
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required


class Private(View):
    def get(self, request):
        response = JsonResponse({"get_private": "ok"})
        return response

    def post(self, request):
        user = request.user
        response = JsonResponse({"username": user})
        return response
