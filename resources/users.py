#: ATTENTION!! < # noinspection > prefixed comments are only
#: for pycharm to ignore PEP 8 style highlights

import json

from flask import Blueprint, make_response

from flask_restful import Api, fields, Resource, marshal, reqparse

from models import User

user_field = {
    'username': fields.String,
}


class UserList(Resource):
    """User list class
    :inherit: - Resource from flask_restful
    :methods: - get()
              - post()
    """
    def __init__(self):
        """Constructor"""
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'username',
            required=True,
            help='No username provided',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'email',
            required=True,
            help='No email provided',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'password',
            required=True,
            help='No password provided',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'verify_password',
            required=True,
            help='No verify password provided',
            location=['form', 'json']
        )
        super().__init__()

    @staticmethod
    def get():
        """get method
        :decorator: - staticmethod
        :return: - dict with a list of users objects with marshal from flask_restful
        """
        return {'users': [marshal(user, user_field) for user in User.select()]}

    def post(self):
        """post method
        :return: if passwords match:
                    - user object
                    - 201 status code
                 if passwords doesn't match:
                    - make_response from flak with error message
                    - 400 status code
        """
        args = self.reqparse.parse_args()
        if args['password'] == args['verify_password']:
            user = User.create_user(**args)
            return marshal(user, user_field), 201
        return make_response(
            json.dumps({
                'error': 'Passwords don\'t match'
            }), 400)


users_api = Blueprint('resources.users', __name__)
# noinspection PyTypeChecker
# --> user_api
api = Api(users_api)
# noinspection PyTypeChecker
# --> UserList
api.add_resource(UserList, '/users', endpoint='users')
