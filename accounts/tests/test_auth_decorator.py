from django.test import Client, TestCase, RequestFactory
from django.urls import reverse

from ..auth_tools.auth_decorator import login_required
from ..views.private import Private


class AuthDecorator(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()

    def test_get_private_endpoint_responds_403_status_code(self):
        get_request_private = login_required(self.factory.get('/accounts/private'))
        self.assertEqual(get_request_private.status_code, 403)
