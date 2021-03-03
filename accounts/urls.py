from django.urls import path
from .views import check_endpoint_status
from . import sign_up, sign_in


urlpatterns = [
    path('status/', check_endpoint_status, name="check_status"),
    path('signup/', sign_up.SignUp.sign_up, name="create_user"),
    path('signin/', sign_in.SignIn.sign_in, name="create_session")
]
