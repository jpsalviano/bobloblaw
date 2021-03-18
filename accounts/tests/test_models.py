from django.test import TestCase, Client
from django.http import JsonResponse
from django.urls import reverse

from ..models import User


class UserModel(TestCase):
    def test_user_model_class(self):
        self.user = User.objects.create(username="cardoso",
                                        email="cardoso@anon.com",
                                        password="abc123-")
        self.assertTrue(hasattr(self.user, "username"))
        self.assertTrue(hasattr(self.user, "email"))
        self.assertTrue(hasattr(self.user, "password"))
