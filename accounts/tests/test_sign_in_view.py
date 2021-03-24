import json

from django.test import TestCase, Client
from django.urls import reverse
from django.core import exceptions

from ..models import User
from ..views.sign_in import validate_password



class SignIn(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(username="cardoso@anon.com",
                                        password="abc123-")

    def test_sign_in_invalidates_wrong_password_against_stored_hashed(self):
        entered_password = "-abc123"
        self.assertEqual(len(self.user.password), 60)
        with self.assertRaises(exceptions.ValidationError) as error:
            validate_password(entered_password, self.user.password)
        self.assertEqual(error.exception.message, "Wrong password.")

    def test_sign_in_validates_right_password_against_stored_hashed(self):
        password_txt = "abc123-"
        validate_password(password_txt, self.user.password)

    def test_sign_in_responds_error_if_wrong_password_is_entered(self):
        payload = {"username": "cardoso@anon.com", "password": "-abc123"}
        expected_result = {"error": ["Wrong password."]}
        result = self.client.post(reverse("sign_in"), payload, content_type="application/json")
        self.assertEqual(result.json(), expected_result)
        self.assertEqual(result.status_code, 401)

    def test_sign_in_responds_error_if_non_existent_username_is_entered(self):
        payload = {"username": "cardoso123@anon.com", "password": "-aasdfsa#bc123"}
        expected_result = {"error": ["Username does not exist."]}
        result = self.client.post(reverse("sign_in"), payload, content_type="application/json")
        self.assertEqual(result.json(), expected_result)
        self.assertEqual(result.status_code, 401)
