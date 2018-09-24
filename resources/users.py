import json

from flask import Blueprint, make_response

from flask_restful import Api, fields, Resource, marshal, reqparse

from models import User

user_field = {
    'username': fields.String,
}


class UserList(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'username',
            required=True,
            help='No username was provided',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'email',
            required=True,
            help='No email was provided',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'password',
            required=True,
            help='No password was provided',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'verify_password',
            required=True,
            help='No password verification was provided',
            location=['form', 'json']
        )
        super().__init__()

    @staticmethod
    def get():
        return {'users': [marshal(user, user_field) for user in User.select()]}

    def post(self):
        args = self.reqparse.parse_args()
        if args['password'] == args['verify_password']:
            user = User.create_user(**args)
            return marshal(user, user_field), 201
        return make_response(
            json.dumps({
                'error': 'Password and password verification do not match'
            }), 400)


users_api = Blueprint('resources.users', __name__)
# noinspection PyTypeChecker
# --> user_api
api = Api(users_api)
# noinspection PyTypeChecker
# --> UserList
api.add_resource(UserList, '/users', endpoint='users')
