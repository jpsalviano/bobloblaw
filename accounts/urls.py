from django.urls import path, include
from .views.status import check_endpoint_status
from .views.sign_up import SignUp
from .views.sign_in import SignIn
from .views.private import Private



urlpatterns = [
    path("signup/", SignUp.as_view(), name="create_user"),
    path("signin/", SignIn.as_view(), name="sign_in"),
    path("private/", Private.as_view(), name="private"),
]
