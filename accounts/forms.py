from .models import UserFormClass
from django.forms import ModelForm


class SignUpForm(ModelForm):
    
    class Meta:
        model = UserFormClass
        fields = ["username", "email", "password", "password2"]