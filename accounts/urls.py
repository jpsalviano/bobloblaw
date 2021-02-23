from django.urls import path
from .views import check_endpoint_status, signup


urlpatterns = [
    path('status/', check_endpoint_status),
    path('signup/', signup)
]
