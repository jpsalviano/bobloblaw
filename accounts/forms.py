from django import forms

from .models import User


class UserForm(forms.ModelForm):
    username = forms.EmailField(min_length=5, max_length=254)
    password = forms.CharField(min_length=7, max_length=72)

    class Meta:
        model = User
        fields = ["username", "password"]


class SignInForm(forms.Form):
    username = forms.EmailField(min_length=5, max_length=254)
    password = forms.CharField(min_length=7, max_length=72)

