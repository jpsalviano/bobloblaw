from django.views import View
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required


class Private(View):
    def post(self, request):
        user = request.user
        response = JsonResponse({"username": user})
        return response
