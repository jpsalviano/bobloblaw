from django.urls import path
from .views import check_endpoint_status
from . import sign_up


urlpatterns = [
    path('status/', check_endpoint_status, name="check-status"),
    path('signup/', sign_up.SignUp.sign_up, name="create-user"),
#    path('signin/', sign_in.SignIn)
]
