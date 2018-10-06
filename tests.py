import unittest
import copy
from playhouse.test_utils import test_database

from peewee import *

from app import app
from models import Todo, User


DB = SqliteDatabase(':memory:')


class BaseTest(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

        DB.connect()
        DB.create_tables([User, Todo], safe=True)

    def tearDown(self):
        DB.drop_tables(User, Todo)
        DB.close()


class ModelResourcesTest(BaseTest):
    data = {
            'username': 'test_1',
            'email': 'example@mail.com',
            'password': 'password',
            'verify_password': 'password'
        }

    @staticmethod
    def create_user(prefix=None):
        User.create_user(
            username=f'{prefix}_user',
            email=f'example_{prefix}@mail.com',
            password='password'
        )

    def test_create_user(self):
        with test_database(DB, (User, )):
            self.create_user('test_1')
            self.assertEqual(len(User.select()), 1)
            response = self.app.get('/api/v1/users')
            self.assertEqual(User.select().get().username, 'test_1_user')
            self.assertEqual(response.status_code, 200)

    def test_create_new_user(self):
        with test_database(DB, (User,)):
            response = self.app.post('/api/v1/users', data=self.data)
            self.assertEqual(response.status_code, 201)

    def test_create_todo(self):
        with test_database(DB, (Todo,)):
            self.create_user('test_2')
            user = User.select().get()
            Todo.create(name='Walk Tomika', created_by=user.id)
            self.assertEqual(len(Todo.select()), 1)
            response = self.app.post('/api/v1/todos')
            self.assertEqual(response.status_code, 200)


class ViewTest(BaseTest):
    def test_my_todos(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
