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

        @classmethod
        def create_user(cls, username, email, password):
            user = cls(username=username, email=email, password=password)
            return user


    def test_user_model_class(cls):
        doc = cls.TestUser(username="cardoso", email="cardoso@anon.com", password="abc123-")
        result = User(username="cardoso", email="cardoso@anon.com", password="abc123-")
        cls.assertEqual(result.username, doc.username)
        cls.assertEqual(result.email, doc.email)
        cls.assertEqual(result.password, doc.password)

    def test_user_model_create_user_method(cls):
        doc = cls.TestUser.create_user(username="cardoso", email="cardoso@anon.com", password="abc123-")
        result = User.create_user(username="cardoso", email="cardoso@anon.com", password="abc123-")
        cls.assertEqual(result.username, doc.username)
        cls.assertEqual(result.email, doc.email)
        cls.assertEqual(result.password, doc.password)


class EndpointStatusTestCase(TestCase):
    def test_check_endpoint_status(self):
        doc = JsonResponse({'status': 'ok'})
        request = client.get("status/")
        self.assertEqual(check_endpoint_status(request).content, doc.content)
        self.assertEqual(check_endpoint_status(request).status_code, doc.status_code)


class SignUpTestCase(TestCase):
    def setUp(self):
        User.create_user(username="cardoso", email="cardoso@anon.com", password="abc123-")