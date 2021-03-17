from django.core import exceptions, serializers


def deserialize_sign_up_form(payload):
    # Checks if all required fields are filled and if both passwords match
    try:
        # TODO: extract strings and set to vars: username, email, password, password2
        # deserialized is a generator; how to handle it?
        fields = ["username", "email", "password", "password2"]
        for obj in serializers.deserialize("json", payload):
            fields.append(obj)
    except KeyError as error:
        error = str(error).title().strip("'")
        if "Password" in error:
            raise exceptions.ValidationError("Password must be entered twice.")
        raise exceptions.ValidationError(f"{error} must be provided.")
    #else: return username, password, email -> so UserForm can be instantiated for the rest of the validation