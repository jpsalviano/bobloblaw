from django import forms

from .models import User


class SignUpForm(forms.ModelForm):
    username = forms.CharField(min_length=5, max_length=20)
    email = forms.EmailField(max_length=254)
    password = forms.CharField(min_length=7, max_length=72)

    class Meta:
        model = User
        fields = ["username", "email", "password"]
