from django import forms

from .models import User


class UserForm(forms.ModelForm):
    username = forms.EmailField(max_length=254)
    password = forms.CharField(min_length=7, max_length=72)

    class Meta:
        model = User
        fields = ["username", "password"]
