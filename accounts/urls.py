from django.urls import path
from .views.status import check_endpoint_status
from .views.sign_up import SignUp
from .views.sign_in import SignIn
from .views.auth_jwt import GenerateToken



urlpatterns = [
    path("signup/", SignUp.as_view(), name="create_user"),
    path("signin/", SignIn.as_view(), name="sign_in"),
    path("auth_jwt/", GenerateToken.as_view(), name="auth_jwt")
]
