import json

from .models import User

class SignIn:
    def sign_in(request):
        if request.method == 'POST':
            data = json.loads(request.body.decode())
            user = User.sign_in(data)
