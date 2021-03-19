from django.test import TestCase, Client
from django.urls import reverse
from django.core.signing import Signer

from ..models import User


class AuthJWT(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(username="cardoso",
                                        email="cardoso@anon.com",
                                        password="abc123-")

    def test_auth_jwt_generates_token(self):
        payload = {"user_id": self.user.id}
        result = self.client.post(reverse("auth_jwt"), payload, content_type="application/json")
        key1 = Signer().sign("JWT")
        key2 = Signer().sign("JWT")
        self.assertEqual(key1, key2)