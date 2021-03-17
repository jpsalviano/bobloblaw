from django.core import exceptions, serializers


def deserialize_sign_up_form(payload):
    # Checks if all required fields are filled and if both passwords match
    try:
        deserialized = serializers.deserialize("json", payload, ignorenonexistent=False)
        # TODO: extract strings and set to vars: username, email, password, password2
        # deserialized is a generator; how to handle it?
        assert password == password2
    except KeyError as error:
        error = str(error).title().strip("'")
        if "Password" in error:
            raise exceptions.ValidationError("Password must be entered twice.")
        raise exceptions.ValidationError(f"{error} must be provided.")
    except AssertionError:
        raise exceptions.ValidationError("Passwords do not match.")