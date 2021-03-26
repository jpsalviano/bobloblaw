from django.views import View
from django.http import HttpResponse


class Private(View):
    def get(self, request):
        return HttpResponse("This is a private endpoint.")
