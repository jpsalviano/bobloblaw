import json
import bcrypt
from secrets import token_hex

from .models import User, Session

class SignIn:
    def sign_in(request):
        try:
            request.method == 'POST'
            create_session_data = json.loads(request.body)
            user = User.objects.get(username=create_session_data["username"])
            SignIn.check_password(user.id, create_session_data["password"])
            session = Session.objects.create(user_id=user.id, session_token=SignIn.create_session_token())
        except Exception as e:
            raise e
        else:
            session.save()
            response = HttpResponse()
            response.COOKIES = {"session_token": session.session_token}
            response.status_code = 200
            return response

    @classmethod
    def check_password(cls, user_id, entered_password):
        stored_password = User.objects.get(id=user_id).password
        return bcrypt.checkpw(entered_password.encode(), stored_password)

    @classmethod
    def create_session_token(cls):
        return token_hex(32)