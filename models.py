#: ATTENTION!! < # noinspection > prefixed comments are only
#: for pycharm to ignore PEP 8 style highlights

import datetime

from argon2 import PasswordHasher
# from itsdangerous import (TimedJSONWebSignatureSerializer as T_jwss,
#                           BadSignature, SignatureExpired)
from peewee import *

# from config import SECRET_KEY

# Database init
DATABASE = SqliteDatabase('todos.sqlite')

# PasswordHasher() instance
HASHER = PasswordHasher()


class User(Model):
    """
    User Model
    :inherit: Model class from peewee
    :fields: - username - CharField(), unique
             - email - CharField(), unique
             - password - CharField()
    """
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField()

    class Meta:
        database = DATABASE

    # noinspection PyUnusedLocal
    #   --> **kwargs
    @classmethod
    def create_user(cls, username, email, password, **kwargs):
        """Classmethod create user
        :param: - username
                - email
                - password
        """
        email = email.lower()
        try:
            cls.select().where((cls.email == email) |
                               (cls.username**username)).get()
        except cls.DoesNotExist:
            user = cls(username=username, email=email)
            user.password = user.set_password(password)
            user.save()
            return user
        else:
            raise Exception("User with that email or username already exists")

    @staticmethod
    def set_password(password):
        """set password with PasswordHasher.hash()
        :parameter: - password
        :return: - hashed password
        """
        return HASHER.hash(password)

    def verify_password(self, password):
        """verify password with PasswordHasher.verify()
        :parameter: - password
        :return: - verified password
        """
        # noinspection PyTypeChecker
        # --> self.password
        return HASHER.verify(self.password, password)

    # Before unit 10 update on Treehouse, it was required,
    # It can be tested in POSTMAN, no front-end implementation to use back-end API auth
    # @staticmethod
    # def verify_auth_token(token):
    #     serializer = T_jwss(SECRET_KEY)
    #     try:
    #         data = serializer.loads(token)
    #     except (SignatureExpired, BadSignature):
    #         return None
    #     else:
    #         # noinspection PyUnresolvedReferences
    #         # --> .id
    #         user = User.get(User.id == data['id'])
    #         return user
    #
    # def generate_auth_token(self, expires=3600):
    #     serializer = T_jwss(SECRET_KEY, expires_in=expires)
    #     return serializer.dumps({'id': self.id})
    #######################################################


class Todo(Model):
    """
    Todo_s Model
    :inherit: Model class from peewee
    :fields: - name - CharField()
             - created_at - DateTimeField(), default now
             - created_by - ForeignKeyField(), User
    """
    name = CharField()
    created_at = DateTimeField(default=datetime.datetime.now)
    created_by = ForeignKeyField(User, related_name='todos_set')

    class Meta:
        database = DATABASE


def initialize():
    """Initializing DATABASE"""
    DATABASE.connect()
    DATABASE.create_tables([User, Todo], safe=True)
    DATABASE.close()
