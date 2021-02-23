from django.urls import path
from .views import check_endpoint_status


urlpatterns = [
    path('status/', check_endpoint_status)
]
