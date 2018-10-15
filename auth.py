from flask import g

from flask_httpauth import HTTPBasicAuth

from models import User

auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(email_or_username, password):
    """Verify password -
    :decorator: - basic_auth.verify_password
    :param: - email_or_username - for verification email or username
            - password
    """
    try:
        user = User.get((User.username == email_or_username) |
                        (User.email == email_or_username))
        if not user.verify_password(password):
            return False
    except User.DoesNotExist:
        return False
    else:
        g.user = user
        return True
