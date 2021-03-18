from django.test import TestCase, Client
from django.http import JsonResponse
from django.urls import reverse

from ..models import User


class EndpointStatus(TestCase):
    def setUp(self):
        self.client = Client()

    def test_check_endpoint_status(self):
        expected_result = JsonResponse({"status": "ok"})
        result = self.client.get(reverse('check_status'))
        self.assertEqual(result.content, expected_result.content)
        self.assertEqual(result.status_code, 200)


class ModelsTests(TestCase):
    def test_user_model_class(self):
        self.user = User.objects.create(username="cardoso",
                                        email="cardoso@anon.com",
                                        password="abc123-")
        self.assertTrue(hasattr(self.user, "username"))
        self.assertTrue(hasattr(self.user, "email"))
        self.assertTrue(hasattr(self.user, "password"))
