#: ATTENTION!! < # noinspection > prefixed comments are only
#: for pycharm to ignore PEP 8 style highlights

import json

from flask import abort, Blueprint, g, make_response, url_for

from flask_restful import (Api, fields, Resource, marshal,
                           marshal_with, reqparse)

from auth import auth
from models import Todo


todo_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'created_at': fields.DateTime
}


def object_or_404(id):
    try:
        # noinspection PyUnresolvedReferences
        # --> .id
        todo = Todo.get(Todo.id == id)
    except Todo.DoesNotExist:
        abort(404)
    else:
        return todo


class TodoList(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'name',
            required=True,
            help='No todo title was provided',
            location=['form', 'json']
        )
        super().__init__()

    def get(self):
        return [marshal(todo, todo_fields) for todo in Todo.select()]

    @marshal_with(todo_fields)
    @auth.login_required
    def post(self):
        args = self.reqparse.parse_args()
        todo = Todo.create(created_by=g.user, **args)
        return (todo, 201,
                {'Location': url_for('resources.todos.todo', id=todo.id)})


class Todos(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'name',
            required=True,
            help='No todo title was provided',
            location=['form', 'json']
        )
        super().__init__()

    @marshal_with(todo_fields)
    def get(self, id):
        return object_or_404(id)

    @marshal_with(todo_fields)
    @auth.login_required
    def put(self, id):
        args = self.reqparse.parse_args()
        try:
            # noinspection PyUnresolvedReferences
            # --> .id
            todo = Todo.select().where(
                Todo.created_by == g.user,
                Todo.id == id
            ).get()
        except Todo.DoesNotExist:
            return make_response(json.dumps(
                    {'error': 'That todo does not exist or is not editable'}
                ), 403)
        query = todo.update(**args)
        query.execute()
        todo = object_or_404(id)
        return (todo, 200, {
                'Location': url_for('resources.todos.todo', id=id)})

    @auth.login_required
    def delete(self, id):
        try:
            # noinspection PyUnresolvedReferences
            # --> .id
            todo = Todo.select().where(
                Todo.created_by == g.user,
                Todo.id == id
            ).get()
        except Todo.DoesNotExist:
            return make_response(json.dumps(
                    {'error': 'That todo does not exist or is not deletable'}
                ), 403)
        query = todo.delete()
        query.execute()
        return '', 204, {'Location': url_for('resources.todos.todo')}


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
