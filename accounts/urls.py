from django.urls import path
from .views import check_endpoint_status
from .sign_up import SignUp
from .sign_in import SignIn


urlpatterns = [
    path('status/', check_endpoint_status, name="check_status"),
    path('signup/', SignUp.sign_up, name="create_user"),
    path('signin/', SignIn.sign_in, name="create_session")
]
