import unittest
import string
from playhouse.test_utils import test_database

from peewee import *

from app import app
from models import Todo, User


DB = SqliteDatabase(':memory:')
DB.connect()
DB.create_tables([User, Todo], safe=True)


class UserTestCase(unittest.TestCase):
    @staticmethod
    def create(prefix=None):
        User.create_user(
            username=f'{prefix}_user',
            email=f'example_{prefix}@mail.com',
            password='password'
        )


class TodoTestCase(unittest.TestCase):
    @staticmethod
    def create():
        UserTestCase.create('test_2')
        user = User.select().get()
        Todo.create(name='Walk Tomika', created_by=user.id)

    def test_todo_create(self):
        with test_database(DB, (Todo,)):
            self.create()
            self.assertEqual(Todo.select().count(), 1)

    def tearDown(self):
        DB.drop_tables(User, Todo)
        DB.close()


if __name__ == '__main__':
    unittest.main()