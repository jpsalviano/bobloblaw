from django.urls import path
from .views import check_endpoint_status
from . import sign_up


urlpatterns = [
    path('status/', check_endpoint_status),
    path('signup/', sign_up.SignUp),
#    path('signin/', sign_in.SignIn)
]
