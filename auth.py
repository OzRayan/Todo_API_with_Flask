from flask import g

from flask_httpauth import HTTPBasicAuth    # HTTPTokenAuth, MultiAuth

from models import User

auth = HTTPBasicAuth()
# token_auth = HTTPTokenAuth(scheme='Token')
# auth = MultiAuth(token_auth, basic_auth)


@auth.verify_password
def verify_password(username, password):
    """Verify password -
    :decorator: - basic_auth.verify_password
    :param: - email_or_username
            - password
    """
    try:
        user = User.get(User.username == username)
        if not user.verify_password(password):
            return False
    except User.DoesNotExist:
        return False
    else:
        g.user = user
        return True

# TOKEN-BASED AUTHENTICATION
# @token_auth.verify_token
# def verify_token(token):
#     """Verify token
#     :decorator: - token_auth.verify_token
#     :param: - token
#     """
#     user = User.verify_auth_token(token)
#     if user is not None:
#         g.user = user
#         return True
#     return False
