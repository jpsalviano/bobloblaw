from django.test import Client, TestCase
from django.core.signing import Signer

from ..models import User
from ..auth_tools.auth_jwt import _generate_token
from ..auth_tools.auth_decorator import login_required


class AuthDecorator(TestCase):
    pass