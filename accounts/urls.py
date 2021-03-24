from django.urls import path
from .views.status import check_endpoint_status
from .views.sign_up import SignUp
from .views.sign_in import SignIn



urlpatterns = [
    path("signup/", SignUp.as_view(), name="create_user"),
    path("signin/", SignIn.as_view(), name="sign_in"),
]
