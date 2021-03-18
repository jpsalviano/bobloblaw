import json

from django.test import TestCase, Client
from django.urls import reverse
from django.http import JsonResponse
from django.core import exceptions

from ..models import User
from ..views.sign_in import SignIn, validate_password



class SignIn(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(username="cardoso",
                                        email="cardoso@anon.com",
                                        password="abc123-")

    def test_sign_in_invalidates_wrong_password_against_stored_hashed(self):
        entered_password = "-abc123"
        self.assertEqual(len(self.user.password), 60)
        with self.assertRaises(exceptions.ValidationError) as error:
            validate_password(entered_password, self.user.password)
        self.assertEqual(error.exception.message, "Wrong password.")

    def test_sign_in_validates_right_password_against_stored_hashed(self):
        entered_password = "abc123-"
        validate_password(entered_password, self.user.password)

'''    def test_sign_in_creates_and_responds_session_token(self):
        payload = {"username": "cardoso", "password": "abc123-"}
        result = self.client.post(reverse("create_session"), payload, content_type="application/json")
        self.assertEqual(len(result.json()["session_token"]), 64)
        self.assertEqual(result.status_code, 201)
        session = Session.objects.get(user=self.user.id)
        self.assertTrue(hasattr(session, "session_token"))
        self.assertEqual(len(session.session_token), 64)
        self.assertEqual(session.session_token, result.json()["session_token"])

    def test_sign_in_does_not_validate_wrong_password(self):
        payload = {"username": "cardoso", "password": "-abc123"}
        expected_result = {"error": "Wrong password."}
        result = self.client.post(reverse("create_session"), payload, content_type="application/json")
        self.assertEqual(result.json(), expected_result)
        self.assertEqual(result.status_code, 403)
        session = Session.objects.filter(user=self.user.id)
        self.assertFalse(session.exists())

    def test_sign_in_responds_error_non_existent_username_is_entered(self):
        payload = {"username": "cardoso123", "password": "-abc123"}
        expected_result = {"error": "Username does not exist."}
        result = self.client.post(reverse("create_session"), payload, content_type="application/json")
        self.assertEqual(result.json(), expected_result)
        self.assertEqual(result.status_code, 403)'''
