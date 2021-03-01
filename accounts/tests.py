from django.test import TestCase, Client
from django.db import models
from django.http import JsonResponse

from .models import User
from .views import check_endpoint_status, SignUp


client = Client(HTTP_USER_AGENT='Mozilla/5.0')


class UserModelTestCase(TestCase):
    
    class TestUser(models.Model):
        username = models.CharField(max_length=30, unique=True)
        email = models.EmailField()
        password = models.CharField(max_length=100)

    def test_create_user_class_method(cls):
        doc = cls.TestUser(username="cardoso", email="cardoso@anon.com", password="abc123-")
        self.assertNotEqual(User)


class EndpointStatusTestCase(TestCase):
    def test_check_endpoint_status(self):
        doc = JsonResponse({'status': 'ok'})
        request = client.get("status/")
        self.assertEqual(check_endpoint_status(request).content, doc.content)
        self.assertEqual(check_endpoint_status(request).content, doc.content)


class SignUpTestCase(TestCase):
    def setUp(self):
        User.create_user(username="cardoso", email="cardoso@anon.com", password="abc123-")
