from .models import User
from django.forms import ModelForm


class SignUpForm(ModelForm):
    class Meta:
        model = User
        fields = ["username", "email", "password"]
