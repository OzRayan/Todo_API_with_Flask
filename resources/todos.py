#: ATTENTION!! < # noinspection > prefixed comments are only
#: for pycharm to ignore PEP 8 style highlights

import json

from flask import abort, Blueprint, g, make_response, url_for

from flask_restful import (Api, fields, Resource, marshal,
                           marshal_with, reqparse)

from auth import auth
from models import Todo


# todo object field
todo_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'created_at': fields.DateTime
}


def object_or_404(id):
    """Get todo object or 404
    :parameter: - id - todo id
    :return: - todo object
    """
    try:
        # noinspection PyUnresolvedReferences
        # --> .id
        todo = Todo.get(Todo.id == id)
    except Todo.DoesNotExist:
        abort(404)
    else:
        return todo


class TodoList(Resource):
    """Todo list class
    :inherit: - Resource from flask_restful
    :methods: - get()
              - post()
    """
    def __init__(self):
        """Constructor"""
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'name',
            required=True,
            help='No todo name was provided',
            location=['form', 'json']
        )
        super().__init__()

    @staticmethod
    def get():
        """get method
        :decorator: - staticmethod
        :return: - list of todo objects with marshal from flask_restful
        """
        return [marshal(todo, todo_fields) for todo in Todo.select()]

    @marshal_with(todo_fields)
    @auth.login_required
    def post(self):
        """post method
        :decorators: - marshal_with from flask_restful
                       :param: todo_fields (defined top)
                     - auth.login_required
        :return: - todo object
                 - 201 status code
                 - location - url for todo object
        """
        args = self.reqparse.parse_args()

        # created_by global user - creates a Todo object
        todo = Todo.create(created_by=g.user, **args)
        return (todo, 201,
                {'Location': url_for('resources.todos.todo', id=todo.id)})


class Todos(Resource):
    """Todo class
    :inherit: - Resource from flask_restful
    :methods: - get()
              - put()
              - delete()
    """
    def __init__(self):
        """Constructor"""
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'name',
            required=True,
            help='No todo title provided',
            location=['form', 'json']
        )
        super().__init__()

    @marshal_with(todo_fields)
    def get(self, id):
        """get method
        :decorator: - marshal_with from flask_restful
                      :param: - todo_fields (defined top)
        :parameter: - id - todo object id
        :return: - object_or_404() method
        """
        return object_or_404(id)

    @auth.login_required
    @marshal_with(todo_fields)
    def put(self, id):
        """put method
        :decorators: - marshal_with from flask_restful
                        :param: todo_fields (defined top)
                     - auth.login_required
        :parameter: - todo id
        :return: if Todo object exist:
                    - todo object
                    - 200 status code
                    - location - url for todo object
                 if Todo object doesn't exist:
                    - make_response from flak with error message
                    - 403 status code
        """
        args = self.reqparse.parse_args()
        try:
            # noinspection PyUnresolvedReferences
            # --> .id
            query = Todo.update(**args).where(
                Todo.created_by == g.user,
                Todo.id == id)
            query.execute()
            todo = object_or_404(id)
            return (todo, 200, {
                'Location': url_for('resources.todos.todo', id=id)})

        except Todo.DoesNotExist:
            return make_response(json.dumps(
                    {'error': 'That todo does not exist or is not editable'}
                ), 404)

    @auth.login_required
    def delete(self, id):
        """delete method
        :decorators: - auth.login_required
        :parameter: - todo id
        :return: if Todo object exist:
                    - empty string
                    - 204 status code
                 if Todo object doesn't exist:
                    - make_response from flak with error message
                    - 403 status code
        """
        try:
            # noinspection PyUnresolvedReferences
            # --> .id
            query = Todo.delete().where(
                Todo.created_by == g.user,
                Todo.id == id)
            query.execute()
            return '', 204
        except Todo.DoesNotExist:
            return make_response(json.dumps(
                    {'error': 'That todo does not exist or is not deletable'}
                ), 403)


todo_api = Blueprint('resources.todos', __name__)
# noinspection PyTypeChecker
# --> todo_api
api = Api(todo_api)
# noinspection PyTypeChecker
# --> TodoList
api.add_resource(TodoList, '/todos', endpoint='todos')
# noinspection PyTypeChecker
# --> Todos
api.add_resource(Todos, '/todos/<int:id>', endpoint='todo')
